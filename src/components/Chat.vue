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
      messagesLoaded: false,
      currentUserId: this.$store.state.id,
      fiId: null,
      receptionRoom: null,
      messagesByBot: null,
      username: this.$store.state.username
    };
  },
  mounted() {
    if (this.$store.state.auth) this.fetchRooms(), this.setFi(), this.dbVars()
    else this.dialog = true;
  },

  destroyed() {
    this.resetRooms();
  },
  methods: {
    async tonijevafunkcija() {
      var user = this.username;
      console.log(user);
      let response = await Camunda.tonijevafunkcija(user);
      console.log(response);
    },
    async dbVars() {
      var user = this.username
      console.log(user)
      let response = await Camunda.getVars(user);
      console.log(response)
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
        const roomContacts = room.users.filter((user) => user._id !== this.currentUserId);
        debugger;
        room.roomName = room.roomName + " - " + 
        roomContacts.map((user) => (user.firstName)) + " " + roomContacts.map((user) => (user.lastName))
        const roomAvatar =
          roomContacts.length === 1 && roomContacts[0].avatar
            ? roomContacts[0].avatar
            : require("../../public/Fi-mini.png");
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
        var processes = await Camunda.getProcesses();
        let iterator = 1;
        let content = "Hej! Dobrodošao. Izaberi proces:";
        const message = {
          room_id: this.receptionRoom,
          sender_id: this.fiId,
          content,
          timestamp: new Date(),
          seen: false,
        };
        await Messages.addMessage(message);

        for (const process of processes) {
          const message1 = {
            room_id: this.receptionRoom,
            sender_id: this.fiId,
            content: iterator + ". " + process.name,
            timestamp: new Date(),
            seen: false,
          };
          await Messages.addMessage(message1);

          iterator++;
        }
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
      await this.setReception();
      await this.introMessage();

      let messages = await Messages.getRoomMessages(room.roomId);
      messages.map((message) => {
        if (this.selectedRoom !== room.roomId) return;
        if (!messages) this.messagesLoaded = true;
        messageList[iterator] = {
          _id: message.id.$oid,
          content: message.content,
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
        this.getLastRoomMessage(room.roomId);
      }, 9000);
      this.refreshMessages(room.roomId);
    },

    async refreshMessages(roomId) {
      const messageList = [];
      let iterator = 0;
      let messages = await Messages.getRoomMessages(roomId);
      messages.map((message) => {
        messageList[iterator] = {
          _id: message.id.$oid,
          content: message.content,
          sender_id: message.sender_id.$oid,
        };
        iterator++;
      });
      //this.getLastRoomMessage(roomId);
      this.messages = messageList;
      this.messagesLoaded = true;
    },

    async sendMessage({ content, roomId }) {
      const message = {
        room_id: roomId,
        sender_id: this.currentUserId,
        content,
        timestamp: new Date(),
        seen: false,
      };
      await Messages.addMessage(message);
      this.refreshMessages(roomId);
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

    async getLastRoomMessage(room) {
      //opcenito
      const LastRoomMessage = await Messages.getLastRoomMessage(room);
      if (!(LastRoomMessage === undefined || LastRoomMessage.length == 0))
        this.lastRoomMessage = LastRoomMessage[0].content;
      return LastRoomMessage;
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

    async setReception() {
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
    },
  },
};
</script>

<style lang="scss">
.line-new {
  display: none;
}
</style>