<template>
  <v-container fluid>
    <chat-window
      height="calc(100vh - 90px)"
      :theme="theme"
      :currentUserId="currentUserId"
      :rooms="rooms"
      :loadingRooms="loadingRooms"
      :messages="messages"
      :messagesLoaded="messagesLoaded"
      :styles="styles"
      @sendMessage="sendMessage"
      @fetchMessages="fetchMessages"
    />
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Hej!</v-card-title>
        <v-card-text>Kako bi koristio ovu aplikaciju, trebaš se registrirati ili prijaviti na već postojeći račun.</v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import ChatWindow from "vue-advanced-chat";
import "vue-advanced-chat/dist/vue-advanced-chat.css";
import { Rooms, Users, Messages, Camunda } from "@/services";
import { parseTimestamp, isSameDay } from "@/utils/dates";
import router from "../router";

export default {
  components: {
    ChatWindow,
  },
  data() {
    return {
      dialog: false,
      theme: "light",
      selectedRoom: null,
      loadingRooms: false,
      rooms: [],
      messages: [],
      styles: {
        message: {
          background: "#fff",
          backgroundMe: "#c4e3fc",
          color: "#0a0a0a",
          colorStarted: "#f8f9fa",
        },
      },
      messagesLoaded: false,
      currentUserId: this.$store.state.id,
      username: this.$store.state.username,
      fiId: null,
      studentId: null,
      student: null,
      receptionRoom: null,
      messagesByBot: null,
      lastRoomMessage: null,
      interval: null,
      processes: null,
      temaVariablesFromDb: null,
      variablesFromCamunda: null,
      awaitingResponseDb: null,
      awaitingResponseByDb: null,
      stepsCounter: 1,
      formattedVariables: null,
    };
  },
  computed: {
    lastMessage: function () {
      if (!(this.messages === undefined || this.messages.length == 0)) {
        return [
          {
            sender: this.messages[this.messages.length - 1].sender_id,
            content: this.messages[this.messages.length - 1].content,
          },
        ];
      }
      return "None";
    },
    awaitingResponse: function () {
      return this.awaitingResponseDb;
    },
    awaitingResponseBy: function () {
      return this.awaitingResponseByDb;
    },
  },
  mounted() {
    if (this.$store.state.auth)
      this.fetchRooms(), this.setFi(), this.getVariables();
    else this.dialog = true;
  },
  destroyed() {
    this.resetRooms();
    clearInterval(this.interval);
  },
  methods: {
    async getAssignee() {
      var username = this.username;
      let response = await Camunda.getCurrentTaskAssignee(username);
      return response;
    },
    async getVariables() {
      var username = this.username;
      this.variablesFromCamunda = await Camunda.getTaskVariables(username);
      console.log(
        "Dohvaćene varijable iz Camunde: ",
        this.variablesFromCamunda
      );
      return this.variablesFromCamunda;
    },
    resetRooms() {
      this.loadingRooms = true;
      this.rooms = [];
      this.resetMessages();
    },
    resetMessages() {
      this.messages = [];
      this.messagesLoaded = false;
    },
    async fetchRooms() {
      this.resetRooms();
      const rooms = await Rooms.getUserRooms(this.currentUserId);

      const roomList = [];
      const rawRoomUsers = [];
      const rawMessages = [];

      rooms.map((room) => {
        roomList[room.roomId.$oid] = {
          roomId: room.roomId.$oid,
          awaitingResponse: room.awaitingResponse,
          awaitingResponseBy: room.awaitingResponseBy,
          roomName: room.roomName,
          users: [],
        };
        const rawUsers = [];
        room.users.map((userId) => {
          const promise = Users.getOne(userId.$oid).then((user) => {
            return {
              _id: user[0].id.$oid,
              username: user[0].firstName,
              roomId: room.roomId.$oid,
              firstName: user[0].firstName,
              lastName: user[0].lastName,
            };
          });

          rawUsers.push(promise);
        });

        rawUsers.map((users) => rawRoomUsers.push(users));
        rawMessages.push(this.getLastMessage(room.roomId.$oid));
      });

      const users = await Promise.all(rawRoomUsers);

      users.map((user) => {
        roomList[user.roomId].users.push(user);
      });

      const roomMessages = await Promise.all(rawMessages).then((messages) => {
        return messages.map((message) => {
          return {
            lastMessage: this.formatLastMessage(message),
            roomId: message.roomId,
          };
        });
      });
      roomMessages.map((ms) => {
        roomList[ms.roomId].lastMessage = ms.lastMessage;
      });

      const formattedRooms = [];
      Object.keys(roomList).forEach((key) => {
        const room = roomList[key];
        const roomContacts = room.users.filter(
          (user) => user._id !== this.currentUserId
        );
        room.roomName =
          room.roomName +
          " - " +
          roomContacts.map((user) => {
            if (user.firstName === "Fi") return " " + user.firstName;
            else return " " + user.firstName + " " + user.lastName;
          });
        const roomAvatar =
          roomContacts.length === 1 && roomContacts[0].username === "Fi"
            ? require("../../public/Fi-mini.png")
            : require("../../public/icon.png");
        formattedRooms.push({
          ...{
            roomId: key,
            avatar: roomAvatar,
            ...room,
          },
        });
      });
      this.rooms = this.rooms.concat(formattedRooms);
      this.loadingRooms = false;
    },

    async introMessage() {
      if (
        this.selectedRoom == this.receptionRoom &&
        this.messagesByBot == false
      ) {
        this.processes = await Camunda.getProcesses();
        let iterator = 1;
        let content = "Hej! Dobrodošao. Izaberi proces:";
        const message = {
          room_id: this.receptionRoom,
          sender_id: this.fiId,
          username: "Fi",
          content,
          timestamp: new Date(),
          seen: false,
        };
        await Messages.addMessage(message);

        for (const process of this.processes) {
          const message1 = {
            room_id: this.receptionRoom,
            sender_id: this.fiId,
            username: "Fi",
            content: iterator + ". " + process.name,
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message1);

          iterator++;
        }
        await Rooms.updateRoomField(
          this.selectedRoom,
          "awaitingResponse",
          true
        );
      }
    },

    async fetchMessages({ room, options = {} }) {
      if (options.reset) this.resetMessages();
      clearInterval(this.interval);
      const messageList = [];
      let iterator = 0;
      this.selectedRoom = room.roomId;

      await Users.updateUserField(
        this.currentUserId,
        "selectedRoom",
        room.roomId
      );
      await this.setReceptionAndProcessRooms();
      await this.introMessage();

      let messages = await Messages.getRoomMessages(room.roomId);
      messages.map((message) => {
        if (this.selectedRoom !== room.roomId) return;
        if (!messages) this.messagesLoaded = true;
        messageList[iterator] = {
          _id: message.id.$oid,
          content: message.content,
          username: message.username,
          sender_id: message.sender_id.$oid,
        };
        iterator++;
      });
      this.messages = messageList;
      if (!(messageList === undefined || messageList.length == 0))
        this.lastRoomMessage = messageList[messageList.length - 1].content;
      this.messagesLoaded = true;

      this.markMessagesSeen(room.roomId);
      this.interval = setInterval(() => {
        this.refreshState(room.roomId);
      }, 9000);
      await this.refreshState(room.roomId);
      if (this.selectedRoom == this.receptionRoom)
        this.studentId = this.currentUserId; //ovako postavlja studentId jer jedino studenti imaju recepciju
      if (this.$store.state.processRoomId1 == this.selectedRoom)
        this.prikazPrijaveTeme();
    },

    async refreshState(roomId) {
      let rooms = await Rooms.getUserRooms(this.currentUserId); //updating awaitingresponse and awaitingresponseby computed
      let filtered = rooms.filter((o) => o.roomId.$oid === roomId);
      this.awaitingResponseDb = filtered[0].awaitingResponse;
      this.awaitingResponseByDb = filtered[0].awaitingResponseBy;

      const messageList = [];
      let iterator = 0;
      let messages = await Messages.getRoomMessages(roomId); //updating lastmessage computed
      messages.map((message) => {
        messageList[iterator] = {
          _id: message.id.$oid,
          content: message.content,
          username: message.username,
          sender_id: message.sender_id.$oid,
        };
        iterator++;
      });
      this.messages = messageList;
      this.messagesLoaded = true;
      this.getFlagForRoom(rooms, this.selectedRoom);
    },

    async sendMessage({ content, roomId }) {
      const message = {
        room_id: roomId,
        sender_id: this.currentUserId,
        username: this.username,
        content,
        timestamp: new Date(),
        seen: false,
      };
      await Messages.addMessage(message);
      await this.refreshState(roomId);
      await this.receptionProcessStart();
      await this.odlukaOTemi();
      await this.triggerFi();
      this.formalnaPrijava();
    },

    formatLastMessage(message) {
      if (!message.timestamp) return;
      const date = new Date(message.timestamp);
      const timestampFormat = isSameDay(date, new Date())
        ? "HH:mm"
        : "DD/MM/YY";
      let timestamp = parseTimestamp(message.timestamp, timestampFormat);
      if (timestampFormat === "HH:mm") timestamp = `Today, ${timestamp}`;
      let content = message.content;
      return {
        content,
        sender_id: message.sender_id.$oid,
        timestamp,
        date: message.timestamp,
        seen:
          message.sender_id.$oid === this.currentUserId ? message.seen : null,
        new:
          message.sender_id.$oid !== this.currentUserId &&
          (!message.seen || !message.seen[this.currentUserId]),
      };
    },
    async getLastMessage(room) {
      //za settanje propertija sobe
      const LastRoomMessage = await Messages.getLastRoomMessage(room);
      const array = [];
      LastRoomMessage.map((m) => array.push(m));
      return { ...array[0], roomId: room };
    },

    markMessagesSeen(room) {
      Messages.updateMessageField(room, "seen", true);
    },

    async setFi() {
      let users = await Users.getAll();
      let obj = users.find((o) => o.email === "fibot@unipu.hr");
      this.fiId = obj.id.$oid;
    },

    async setReceptionAndProcessRooms() {
      let userId = this.currentUserId;
      let rooms = await Rooms.getUserRooms(userId);
      let obj = rooms.filter((o) => o.initial === true);
      if (!(obj === undefined || obj.length == 0)) {
        this.receptionRoom = obj[0].roomId.$oid;
        let messages = await Messages.getAll();
        let fiId = this.fiId;
        let msgobj = messages.filter(
          (o) =>
            o.room_id.$oid === obj[0].roomId.$oid && o.sender_id.$oid === fiId
        );
        if (msgobj === undefined || msgobj.length == 0)
          this.messagesByBot = false;
        else this.messagesByBot = true;
      } else {
        this.receptionRoom = "None";
      }

      if (!this.processes) this.processes = await Camunda.getProcesses();

      let processRoom1 = rooms.filter((o) =>
        o.businessKey.includes(this.processes[0].key)
      );
      if (!(processRoom1 === undefined || processRoom1.length == 0)) {
        this.$store.dispatch("setProcessRoomId1", processRoom1[0].roomId.$oid);
      }

      let processRoom2 = rooms.filter((o) =>
        o.businessKey.includes(this.processes[1].key)
      );
      if (!(processRoom2 === undefined || processRoom2.length == 0)) {
        this.$store.dispatch("setProcessRoomId2", processRoom2[0].roomId.$oid);
      }
    },

    async getFlagForRoom(rooms, roomId) {
      if (roomId != this.receptionRoom) {
        let obj = rooms.filter((o) => o.roomId.$oid === roomId);
        if (obj[0].flag == true) this.temaVariablesFromDb = "sent";
        else console.log("Varijable nisu još dohvaćene s baze.");
      }
    },

    async receptionProcessStart() {
      if (
        this.currentUserId != this.fiId &&
        this.selectedRoom == this.receptionRoom &&
        this.awaitingResponse
      )
        await Rooms.updateRoomField(
          this.selectedRoom,
          "awaitingResponse",
          false
        );
      if (this.lastMessage[0].content.includes("1")) {
        await Camunda.StartProcessInstance(
          this.processes[0].key,
          this.processes[0].name,
          this.$store.state.username
        );
        let rooms = await Rooms.getUserRooms(this.currentUserId);
        this.$store.dispatch(
          "setProcessRoomId1",
          rooms[rooms.length - 1].roomId.$oid
        );
        await Users.updateUserField(
          this.currentUserId,
          "selectedRoom",
          rooms[rooms.length - 1].roomId.$oid
        );
        router.push("UserTaskForm");
      } else if (this.lastMessage[0].content.includes("2")) {
        await Camunda.StartProcessInstance(
          this.processes[1].key,
          this.processes[1].name,
          this.$store.state.username
        );
        let rooms = await Rooms.getUserRooms(this.currentUserId);
        this.$store.dispatch(
          "setProcessRoomId2",
          rooms[rooms.length - 1].roomId.$oid
        );
        await Users.updateUserField(
          this.currentUserId,
          "selectedRoom",
          rooms[rooms.length - 1].roomId.$oid
        );
        this.roomId = rooms[rooms.length - 1].roomId.$oid;
        this.selectedRoom = rooms[rooms.length - 1].roomId.$oid;
      }
    },

    async prikazPrijaveTeme() {
      if (
        this.temaVariablesFromDb != "sent" &&
        this.$store.state.processRoomId1 == this.selectedRoom
      ) {
        const variables = await this.getVariables();
        if (
          !(
            variables.databaseVariables === undefined ||
            variables.databaseVariables.length == 0
          )
        ) {
          let content = "Bok! Student vas je odabrao kao mentora.";
          let message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content,
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);
          content = "Pogledajmo njegovu prijavu završnoga rada:";
          message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content,
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);

          variables.databaseVariables.pop();
          await Promise.all(
            variables.databaseVariables.map(async (message) => {
              message.content = message.content.replace("False", "ne");
              message.content = message.content.replace("false", "ne");
              message.content = message.content.replace("True", "da");
              message.timestamp = new Date();
              await Messages.addMessage(message);
            })
          );

          this.temaVariablesFromDb = "sent";

          let assignee = await this.getAssignee();
          let users = await Users.getAll();
          let obj = users.find((o) => o.username === assignee);
          let taskAssignee = obj.firstName + " " + obj.lastName;
          let taskAssigneeUsername = obj.username; //u ovom slučaju settan mentor
          let taskAssigneeId = obj.id.$oid;
          let roomUsers = users.filter(
            (o) => o.selectedRoom === this.selectedRoom
          );
          if (roomUsers.length >= 2) {
            //settamo studenta samo ako je pronađen u gornjem filteru
            let student = roomUsers.find(
              (o) => o.username != taskAssigneeUsername
            ); //settan student kako bismo se mogli obraćati njemu
            this.student = student.firstName;
            this.studentId = student.id.$oid;
          }

          content = `${taskAssignee}, ukoliko ste zainteresirani, napišite 'Da'. Ukoliko niste, 'Ne'.`;
          message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content,
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);

          await Rooms.updateRoomField(
            this.selectedRoom,
            "awaitingResponse",
            true
          );
          await Rooms.updateRoomField(
            this.selectedRoom,
            "awaitingResponseBy",
            taskAssigneeId
          );
        }
        this.refreshState(this.selectedRoom);
      }
    },

    async odlukaOTemi() {
      if (
        Object.prototype.hasOwnProperty.call(
          this.variablesFromCamunda,
          "serviceVariables"
        )
      ) {
        if (
          this.awaitingResponse &&
          this.awaitingResponseBy == this.currentUserId &&
          Object.prototype.hasOwnProperty.call(
            this.variablesFromCamunda.serviceVariables.model,
            "odluka"
          ) &&
          this.$store.state.processRoomId1 == this.selectedRoom
        ) {
          if (
            this.lastMessage[0].content.includes("Da") ||
            this.lastMessage[0].content.includes("da")
          ) {
            let variables = { odluka: { value: "da" } };
            await Camunda.sendTaskVariables(this.username, variables);

            let content = `Odlično, tema je prihvaćena! Dogovorite se oko mogućih izmjena pa me pozovite s naredbom *@Fi* kada ste spremni za formalnu prijavu.`;
            let message = {
              room_id: this.selectedRoom,
              sender_id: this.fiId,
              username: "Fi",
              content,
              timestamp: new Date(),
              seen: false,
            };
            await Messages.addMessage(message);
            await Rooms.updateRoomField(
              this.selectedRoom,
              "awaitingResponse",
              false
            );
            await Rooms.updateRoomField(
              this.selectedRoom,
              "awaitingResponseBy",
              ""
            );
          } else if (
            this.lastMessage[0].content.includes("Ne") ||
            this.lastMessage[0].content.includes("ne")
          ) {
            let variables = { odluka: { value: "ne" } };
            await Camunda.sendTaskVariables(this.username, variables);

            let content =
              "`Nažalost, tvoja tema je odbijena. Možda neki drugi mentor?`;";
            if (this.student) {
              content = `${this.student}, nažalost, tvoja tema je odbijena. Možda neki drugi mentor?`;
            }
            let message = {
              room_id: this.selectedRoom,
              sender_id: this.fiId,
              username: "Fi",
              content,
              timestamp: new Date(),
              seen: false,
            };
            await Messages.addMessage(message);
            await Rooms.updateRoomField(
              this.selectedRoom,
              "awaitingResponse",
              false
            );
            await Rooms.updateRoomField(
              this.selectedRoom,
              "awaitingResponseBy",
              ""
            );
            //TODO: MAKNUTI MENTORA IZ SOBE! maknuti ga iz mongodb chatRooms.users[]
          } else {
            let content = `Ukoliko prihvaćate temu, pošaljite 'Da', inače 'Ne'. `;
            let message = {
              room_id: this.selectedRoom,
              sender_id: this.fiId,
              username: "Fi",
              content,
              timestamp: new Date(),
              seen: false,
            };
            await Messages.addMessage(message);
          }
        }
      }
    },

    async triggerFi() {
      if (
        this.lastMessage[0].content.includes("@Fi") &&
        this.$store.state.processRoomId1 == this.selectedRoom
      ) {
        await Camunda.sendTaskVariables(this.username, null);
        let content = `Super. Krećemo s formalnom prijavom.`;
        let message = {
          room_id: this.selectedRoom,
          sender_id: this.fiId,
          username: "Fi",
          content,
          timestamp: new Date(),
          seen: false,
        };
        await Messages.addMessage(message);
        content = `${this.student}, koji je naslov rada?`;
        message = {
          room_id: this.selectedRoom,
          sender_id: this.fiId,
          username: "Fi",
          content,
          timestamp: new Date(),
          seen: false,
        };
        await Messages.addMessage(message);
        await Rooms.updateRoomField(
          this.selectedRoom,
          "awaitingResponse",
          true
        );
        await Rooms.updateRoomField(
          this.selectedRoom,
          "awaitingResponseBy",
          this.studentId
        );
        await this.refreshState(this.selectedRoom);
      }
    },
    async formalnaPrijava() {
      if (
        this.awaitingResponse &&
        this.awaitingResponseBy == this.currentUserId &&
        this.studentId == this.currentUserId &&
        this.$store.state.processRoomId1 == this.selectedRoom
      ) {
        if (this.stepsCounter == 1) {
          let variables = await this.getVariables();
          this.formattedVariables = variables.model;
          this.formattedVariables.FormalniNaslovRada = {
            value: this.lastMessage[0].content,
          };
          this.stepsCounter++;
          let message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content: "Sazetak problema?",
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);
        } else if (this.stepsCounter == 2) {
          this.formattedVariables.FormalniSazetakProblema = {
            value: this.lastMessage[0].content,
          };
          this.stepsCounter++;
          let message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content: "Dispozicija rada?",
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);
        } else if (this.stepsCounter == 3) {
          this.formattedVariables.FormalnaDispozicijaRada = {
            value: this.lastMessage[0].content,
          };
          this.stepsCounter++;
          let message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content: "Popis literature?",
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);
        } else if (this.stepsCounter == 4) {
          this.formattedVariables.FormalniPopisLiterature = {
            value: this.lastMessage[0].content,
          };
          this.stepsCounter++;
          let message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content: "Mentor?",
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);
        } else if (this.stepsCounter == 5) {
          this.formattedVariables.FormalniMentor = {
            value: this.lastMessage[0].content,
          };
          await Camunda.sendTaskVariables(this.username, this.formattedVariables);
          await this.getVariables()
          let message = {
            room_id: this.selectedRoom,
            sender_id: this.fiId,
            username: "Fi",
            content: "Čestitam! Završni rad je uspješno prijavljen.",
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message);
        }
      }
    },
  },
};
</script>

<style lang="scss">
.line-new {
  display: none;
}
</style>