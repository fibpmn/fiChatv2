<template>
  <div>
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
  </div>
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
    };
  },
  mounted() {
    if (this.$store.state.auth) this.fetchRooms();
    else this.dialog = true;
  },
  destroyed() {
    this.resetRooms();
  },
  methods: {
    async tonijevafunkcija() {
      var user = this.username;
      console.log(user)
      let response = await Camunda.tonijevafunkcija(user);
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

      rooms.forEach((room) => {
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
            roomContacts.map((user) => user.firstName).join(", ") || "Myself";
        const roomAvatar =
          roomContacts.length === 1 && roomContacts[0].avatar
            ? roomContacts[0].avatar
            : require("@/assets/logo.png");
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

    async fetchMessages({ room, options = {} }) {
      if (options.reset) this.resetMessages();

      const messageList = [];
      let iterator = 0;
      let messages = await Messages.getRoomMessages(room.roomId);
      this.selectedRoom = room.roomId;
      await Users.updateUserField(
        this.currentUserId,
        "selectedRoom",
        room.roomId
      );
      messages.forEach((message) => {
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
      this.messagesLoaded = true;
      this.markMessagesSeen(room.roomId);
    },

    async refreshMessages(roomId) {
      const messageList = [];
      let iterator = 0;
      let messages = await Messages.getRoomMessages(roomId);
      messages.forEach((message) => {
        messageList[iterator] = {
          _id: message.id.$oid,
          content: message.content,
          sender_id: message.sender_id.$oid,
        };
        iterator++;
      });
      this.getLastRoomMessage(roomId);
      this.messages = messageList;
      this.messagesLoaded = true;
    },

    async sendMessage({ content, roomId }) {
      debugger;
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
      const LastRoomMessage = await Messages.getLastRoomMessage(room);
      return LastRoomMessage;
    },

    async getLastMessage(room) {
      const LastRoomMessage = await Messages.getLastRoomMessage(room);
      const array = [];
      LastRoomMessage.forEach((m) => array.push(m));
      return { ...array[0], roomId: room };
    },

    markMessagesSeen(room) {
      Messages.updateMessageField(room, "seen", true);
    },
  },
};
</script>

<style lang="scss">
.line-new {
  display: none
}
</style>