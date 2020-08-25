import axios from 'axios'

let Service = axios.create({
    baseURL: 'http://localhost:5000',
    //timeout: 10000
})


let Camunda = {
    async getTaskFormVariables(key) {
        let response = await Service.get(`/api/task/xml/${key}`)
        let doc = response.data
        return {
            model: doc.model,
            schema: doc.schema
        }
    },
}

let Rooms = {
    async getAll() {
        let response = await Service.get('/api/getRooms')
        return response.data.map(doc => {
            return {
                roomId: doc._id,
                roomName: doc.name,
                users: doc.users,
                messages: doc.messages
            };
        });
    },
    async getUserRooms(userid) {
        let response = await Service.get(`/api/getUserRooms/${userid}`)
        return response.data.map(doc => {
            return {
                roomId: doc._id,
                roomName: doc.name,
                users: doc.users,
                messages: doc.messages
            };
        });
    }
}

let Messages = {
    async getAll() {
        let response = await Service.get('/api/getMessages')
        return response.data.map(doc => {
            return {
                id: doc._id,
                room_id: doc.room_id,
                content: doc.content,
                sender_id: doc.sender_id,
                timestamp: doc.timestamp,
                seen: doc.seen
            }
        })
    },
    async getLastRoomMessage(roomid) {
        let response = await Service.get(`/api/getRoomMessages/${roomid}`, {
            params: {
                _limit: 1
            }
        })
        return response.data.map(doc => {
            return {
                id: doc._id,
                room_id: doc.room_id,
                content: doc.content,
                sender_id: doc.sender_id,
                timestamp: doc.timestamp,
                seen: doc.seen
            }
        })
    },
    async getRoomMessages(roomid) {
        let response = await Service.get(`/api/getRoomMessages/${roomid}`)
        return response.data.map(doc => {
            return {
                id: doc._id,
                room_id: doc.room_id,
                content: doc.content,
                sender_id: doc.sender_id,
                timestamp: doc.timestamp,
                seen: doc.seen
            }
        })
    }
}

let Users = {
    async getAll() {
        let response = await Service.get('/api/getUsers')
        return response.data.map(doc => {
            return {
                id: doc._id,
                username: doc.username,
                group: doc.group,
                chatRooms: doc.chatRooms,
                messages: doc.messages
            };
        });
    },
    async getOne(userid) {
        let response = await Service.get(`/api/getUserData/${userid}`)
        return response.data.map(doc => {
            return {
                id: doc._id,
                username: doc.username,
                group: doc.group,
                chatRooms: doc.chatRooms,
                messages: doc.messages
            };
        });
    }
}

// let Files = {
//     getAll() {
//         return Service.get('/api/getFiles')
//     }
// }

export { Service, Rooms, Messages, Users, Camunda }