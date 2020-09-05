<template>
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
</template>

<script>
import ChatWindow from "vue-advanced-chat";
import "vue-advanced-chat/dist/vue-advanced-chat.css";
import { Rooms, Users, Messages } from "@/services";
import { parseTimestamp, isSameDay } from "@/utils/dates";

export default {
  components: {
    ChatWindow,
  },
  props: ["theme", "auth"],
  data() {
    return {
      selectedRoom: null,
      loadingRooms: true,
      rooms: [],
      messages: [],
      messagesLoaded: false,
      start: null,
      end: null,
      roomsListeners: [],
      listeners: [],
      currentUserId: this.$store.state.id,
    };
  },
  mounted() {
    this.fetchRooms();
  },
  destroyed() {
    this.resetRooms();
  },
  methods: {
    resetRooms() {
      this.loadingRooms = true;
      this.rooms = [];
      this.roomsListeners.forEach((listener) => listener());
      this.resetMessages();
    },
    resetMessages() {
      this.messages = [];
      this.messagesLoaded = false;
      this.start = null;
      this.end = null;
      this.listeners.forEach((listener) => listener());
      this.listeners = [];
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
              username: user[0].username,
              roomId: room.roomId.$oid,
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
            roomContacts.map((user) => user.username).join(", ") || "Myself";
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
      if (this.end && !this.start) return (this.messagesLoaded = true);
      const messageList = [];
      let iterator = 0;
      let messages = await Messages.getRoomMessages(room.roomId);
      this.selectedRoom = room.roomId;
      await Rooms.updateUserField(
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
      this.messages = messageList;
    },

    sendMessage({ content, roomId }) {
      const message = {
        room_id: roomId,
        sender_id: this.currentUserId,
        content,
        timestamp: new Date(),
        seen: false,
      };
      Messages.addMessage(message);
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

    async getLastMessage(room) {
      const LastRoomMessage = await Messages.getLastRoomMessage(room);
      const array = [];
      LastRoomMessage.forEach((m) => array.push(m));
      return { ...array[0], roomId: room };
    },

    markMessagesSeen(room, message) {
      if (
        message.sender_id !== this.currentUserId &&
        (!message.seen || !message.seen[this.currentUserId])
      ) {
        this.messagesRef(room.roomId)
          .doc(message.id)
          .update({
            [`seen.${this.currentUserId}`]: new Date(),
          });
      }
    },
  },
};
</script>

