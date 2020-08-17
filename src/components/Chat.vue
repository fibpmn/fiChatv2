<template>
  <chat-window
    height="calc(100vh - 80px)"
    :theme="theme"
    :currentUserId="currentUserId"
    :rooms="rooms"
    :messages="messages"
    :menuActions="menuActions"
  />
</template>

<script>
import ChatWindow from "vue-advanced-chat";
import "vue-advanced-chat/dist/vue-advanced-chat.css";
import { Rooms, Users, Messages } from "@/services";

export default {
  components: {
    ChatWindow,
  },
  props: ["theme"], //id trenutnog usera, pokupiti ga iz bpmna ->getuser()
  data() {
    return {
      rooms: [],
      messages: [],
      messagesLoaded: false,
      start: null,
      end: null,
      roomsListeners: [],
      listeners: [],
      currentUserId: "5f2ed1c620806f9c4fadc693",
      menuActions: [
        {
          //sluzi za gumb na tri veritkalne tocke, ako ces menuActionHandler event za custom akciju
          name: "inviteUser",
          title: "Invite User",
        },
        {
          name: "removeUser",
          title: "Remove User",
        },
        {
          name: "deleteRoom",
          title: "Delete Room",
        },
      ],
      messageActions: [
        {
          name: "replyMessage",
          title: "Reply",
        },
        {
          name: "editMessage",
          title: "Edit Message",
          onlyMe: true,
        },
        {
          name: "deleteMessage",
          title: "Delete Message",
          onlyMe: true,
        },
      ],
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
    this.fetchRooms(), this.fetchUsers(), this.fetchAllMessages();
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
      console.log(rooms);
      const roomList = [];
      const rawRoomUsers = [];
      const rawMessages = [];

      rooms.forEach((room) => {
        roomList[room.id.$oid] = {
          id: room.id.$oid,
          name: room.name,
          messages: room.messages,
          users: room.users,
        };
        const rawUsers = [];
        room.users.map((userId) => {
          const promise = Users.getOne(userId.$oid).then((user) => {
            return {
              id: user[0].id,
              ...{
                username: user[0].username,
                chatRooms: room.id.$oid,
              },
            };
          });
          rawUsers.push(promise);
        });
        rawUsers.map((users) => rawRoomUsers.push(users));
        rawMessages.push();
      });
      const users = await Promise.all(rawRoomUsers);
      users.map((user) => roomList[user.chatRooms].users.push(user));
      //do ovdje ok
      const roomMessages = await Promise.all(rawMessages).then((messages) => {
        return messages.map((message) => {
          return {
            lastMessage: this.formatLastMessage(message),
            roomId: message.roomId,
          };
        });
      });
      roomMessages.map(
        (ms) => (roomList[ms.roomId].lastMessage = ms.lastMessage)
      );
      const formattedRooms = [];
      Object.keys(roomList).forEach((key) => {
        const room = roomList[key];
        const roomContacts = room.users.filter(
          (user) => user._id !== this.currentUserId
        );
        room.roomName =
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
      this.rooms.map((room, index) => this.listenLastMessage(room, index));
    },
    async fetchUsers() {
      var userData = await Users.getAll();
      console.log(userData);
    },
    async fetchAllMessages() {
      var messageData = await Messages.getAll();
      console.log(messageData);
    },
    // async fetchMessages({room, options = {}}){
    //   console.log(room);
    //   if (options.reset) this.resetMessages()
    //   var messageData = await Messages.getAll();
    // },
  },
};
</script>

