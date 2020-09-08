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
import { Rooms, Users, Messages, Camunda } from "@/services";
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
      username: this.$store.state.username,
      styles: {
        general: {
          color: "#0a0a0a",
          backgroundInput: "#fff",
          colorPlaceholder: "#9ca6af",
          colorCaret: "#1976d2",
          colorSpinner: "#333",
          borderStyle: "1px solid #e1e4e8",
          backgroundScrollIcon: "#fff",
        },

        container: {
          border: "none",
          borderRadius: "4px",
          boxShadow: "0px 3px 1px 1px #000",
        },

        header: {
          background: "#fff",
          colorRoomName: "#0a0a0a",
          colorRoomInfo: "#9ca6af",
        },

        footer: {
          background: "#f8f9fa",
          borderStyleInput: "1px solid #e1e4e8",
          borderInputSelected: "#1976d2",
          backgroundReply: "rgba(0, 0, 0, 0.08)",
        },

        content: {
          background: "#f8f9fa",
        },

        sidemenu: {
          background: "#fff",
          backgroundHover: "#f6f6f6",
          backgroundActive: "#e5effa",
          colorActive: "#1976d2",
          borderColorSearch: "#e1e5e8",
        },

        dropdown: {
          background: "#fff",
          backgroundHover: "#f6f6f6",
        },

        message: {
          background: "#fff",
          backgroundMe: "#ccf2cf",
          color: "#0a0a0a",
          colorStarted: "#9ca6af",
          backgroundDeleted: "#dadfe2",
          colorDeleted: "#757e85",
          colorUsername: "#9ca6af",
          colorTimestamp: "#828c94",
          backgroundDate: "#e5effa",
          colorDate: "#505a62",
          backgroundReply: "rgba(0, 0, 0, 0.08)",
          colorReplyUsername: "#0a0a0a",
          colorReply: "#6e6e6e",
          backgroundImage: "#ddd",
          colorNewMessages: "#1976d2",
          backgroundReaction: "#eee",
          borderStyleReaction: "1px solid #eee",
          backgroundReactionHover: "#fff",
          borderStyleReactionHover: "1px solid #ddd",
          colorReactionCounter: "#0a0a0a",
          backgroundReactionMe: "#cfecf5",
          borderStyleReactionMe: "1px solid #3b98b8",
          backgroundReactionHoverMe: "#cfecf5",
          borderStyleReactionHoverMe: "1px solid #3b98b8",
          colorReactionCounterMe: "#0b59b3",
        },

        markdown: {
          background: "rgba(239, 239, 239, 0.7)",
          border: "rgba(212, 212, 212, 0.9)",
          color: "#e01e5a",
          colorMulti: "#0a0a0a",
        },

        room: {
          colorUsername: "#0a0a0a",
          colorMessage: "#67717a",
          colorTimestamp: "#a2aeb8",
          colorStateOnline: "#4caf50",
          colorStateOffline: "#ccc",
        },

        emoji: {
          background: "#fff",
        },

        icons: {
          search: "#9ca6af",
          add: "#1976d2",
          toggle: "#0a0a0a",
          menu: "#0a0a0a",
          close: "#9ca6af",
          closeImage: "#fff",
          file: "#1976d2",
          paperclip: "#1976d2",
          closeOutline: "#000",
          send: "#1976d2",
          sendDisabled: "#9ca6af",
          emoji: "#1976d2",
          emojiReaction: "#828c94",
          document: "#1976d2",
          pencil: "#9e9e9e",
          checkmark: "#0696c7",
          eye: "#fff",
          dropdownMessage: "#fff",
          dropdownMessageBackground: "rgba(0, 0, 0, 0.25)",
          dropdownScroll: "#0a0a0a",
        },
      }, //css
    };
  },
  mounted() {
    this.fetchRooms();
    this.tonijevafunkcija();
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

