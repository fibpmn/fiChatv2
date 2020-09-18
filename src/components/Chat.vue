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
      receptionRoom: null,
      messagesByBot: null,
      lastRoomMessage: null,
      interval: null,
      processes: null,
      variablesFromDb: null,
      variablesFromCamunda: null,
      //dbVariablesToParse: null,
      awaitingResponseDb: null,
      awaitingResponseByDb: null,
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
    if (this.$store.state.auth) this.fetchRooms(), this.setFi()
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
      return this.variablesFromCamunda
    },
    // async parseDbVariables() {
    //   var user = this.username;
    //   this.dbVariablesToParse = await Camunda.parseDatabaseVariables(user);
    //   console.log("Parsirane varijable iz Monga: ", this.dbVariablesToParse);
    // },
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
      if (this.$store.state.processRoomId1 == this.selectedRoom) this.temaTask();
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
      await this.processStart();
      this.sendVariables();
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
      if(roomId != this.receptionRoom){
      let obj = rooms.filter((o) => o.roomId.$oid === roomId);
      if (obj[0].flag == true) this.variablesFromDb = "sent";
      else console.log("Nisu jos poslane varijable.");
      }
    },

    async processStart() {
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
        setTimeout(router.push("UserTaskForm"), 4000);
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

    async temaTask() {
      if (this.variablesFromDb != "sent") {
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
        const variables = await this.getVariables()
        if (!(variables.databaseVariables === undefined || variables.databaseVariables.length == 0)){
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
        this.variablesFromDb = "sent";
        content =
          "Ukoliko ste zainteresirani, napišite 'Da'. Ukoliko niste, 'Ne'.";
        message = {
          room_id: this.selectedRoom,
          sender_id: this.fiId,
          username: "Fi",
          content,
          timestamp: new Date(),
          seen: false,
        };
        await Messages.addMessage(message);
        
        let assignee = await this.getAssignee();
        let users = await Users.getAll();
        let obj = users.find((o) => o.username === assignee);
        let taskAssignee = obj.id.$oid;
        // this.awaitingResponse = true,
        // this.awaitingResponseBy = taskAssignee
        await Rooms.updateRoomField(
          this.selectedRoom,
          "awaitingResponse",
          true
        );
        await Rooms.updateRoomField(
          this.selectedRoom,
          "awaitingResponseBy",
          taskAssignee
        );
        }
        this.refreshState(this.selectedRoom);
      }
    },

    async sendVariables() {
      if (
        this.awaitingResponse &&
        this.awaitingResponseBy == this.currentUserId
      ) {
        if (this.lastMessage[0].content.includes("Da")) {
          console.log("salji varijable");
        } else if (this.lastMessage[0].content.includes("Ne")) {
          console.log("oet salji varijable");
        } else {
          //pls ponovi upis ne kuzim
        }
        //settaj selectedroom na bazi kada je user dodan u sobu jer inace crasha kada se logira
        //gettaskvariables error treba napraviti uvjet
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