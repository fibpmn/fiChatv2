import axios from 'axios'


let Service = axios.create({
    baseURL: 'http://localhost:5000',
    //timeout: 10000
})

let Auth = {
    async RegisterUser(data) {
        let response = await Service.post('/api/users/register', { data })
        return response.data;
    },
    async LoginUser(data) {
        let response = await Service.post('/api/users/login', { data })
        localStorage.setItem('usertoken', response.data.token)
        return "OK"
    },
}

let Camunda = {
    async getCurrentTaskAssignee(user) {
        let response = await Service.get(`/api/${user}/task/assignee`)
        return response.data
    },
    async parseDatabaseVariables(user) {
        let response = await Service.get(`/api/${user}/task/variables/format`)
        return response.data
    },
    //malo veca funkcija, ne znam kako bih ju nazvao
    async getTaskVariables(user) {
        let response = await Service.get(`/api/${user}/task/variables`)
        return response.data;
    },
    async sendTaskVariables(user, variables) {
        await Service.post(`/api/${user}/task/variables`, {variables})
    },
    //GET AVAILABLE PROCESSES
    async getProcesses() {
        let response = await Service.get('/api/process-definitions')
        return response.data.map(doc => {
            return {
                id: doc._id,
                name: doc.name,
                key: doc.key,
            }
        })
    },
    //START PROCES INSTANCE
    async StartProcessInstance(key, name, username) {
        await Service.post(`/api/process-instance/${key}`, { name, username })
    },

    //VUE GENERATOR FORM SPECIFIC, NOT TO BE USED IN CHAT
    async getMentors() {
        let response = await Service.get('/api/mentors')
        let data = Object.values(response.data) 
        return data;
    },
    async getTaskIdForTaskCompletion(username) {
        let response = await Service.get(`/api/task/complete/${username}`) 
        return response.data
    },
    async completeTaskForm(id, variables, username) {
        let response = await Service.post(`/api/task/complete/${id}`, { variables, username })
        return response.data
    },    
}

let Rooms = {
    async getAll() {
        let response = await Service.get('/api/rooms')
        return response.data.map(doc => {
            return {
                roomId: doc._id,
                roomName: doc.name,
                users: doc.users,
                businessKey: doc.businessKey,
                processInstanceId: doc.processInstanceId,
                definitionId: doc.definitionId,
                variables: doc.variables,
                flag: doc.flag,
                initial: doc.initial,
                active: doc.active,
                awaitingResponse: doc.awaitingResponse,
                awaitingResponseBy: doc.awaitingResponseBy
            };
        });
    },
    async getUserRooms(userid) {
        let response = await Service.get(`/api/rooms/${userid}`)
        return response.data.map(doc => {
            return {
                roomId: doc._id,
                roomName: doc.name,
                users: doc.users,
                businessKey: doc.businessKey,
                processInstanceId: doc.processInstanceId,
                definitionId: doc.definitionId,
                variables: doc.variables,
                flag: doc.flag,
                initial: doc.initial,
                active: doc.active,
                awaitingResponse: doc.awaitingResponse,
                awaitingResponseBy: doc.awaitingResponseBy
            };
        });
    },

    async updateRoomField(room, field, value) {
        let response = await Service.put('/api/rooms', {
            room: room,
            field: field,
            value: value
        })
        return response;
    },

    async createRoom(email, fiemail, name){
        await Service.post(`/api/fiRoom`, { email, fiemail, name })
    }
}

let Messages = {
    async getAll() {
        let response = await Service.get('/api/messages')
        return response.data.map(doc => {
            return {
                id: doc._id,
                room_id: doc.room_id,
                content: doc.content,
                sender_id: doc.sender_id,
                username: doc.username,
                timestamp: doc.timestamp,
                seen: doc.seen
            }
        })
    },
    async getLastRoomMessage(roomid) {
        let response = await Service.get(`/api/getLastRoomMessage/${roomid}`)
        return response.data.map(doc => {
            return {
                id: doc._id,
                room_id: doc.room_id,
                content: doc.content,
                username: doc.username,
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
                username: doc.username,
                sender_id: doc.sender_id,
                timestamp: doc.timestamp,
                seen: doc.seen
            }
        })
    },
    async addMessage(message) {
        let response = await Service.post('/api/messages',
            {
                room_id: message.room_id,
                content: message.content,
                sender_id: message.sender_id,
                username: message.username,
                timestamp: message.timestamp,
                seen: message.seen
            })
            return response;
    },

    async updateMessageField(room, field, value) {
        let response = await Service.put('/api/messages', {
            room: room,
            field: field,
            value: value
        })
        return response;
    }
}

let Users = {
    async getAll() {
        let response = await Service.get('/api/users')
        return response.data.map(doc => {
            return {
                id: doc._id,                
                firstName: doc.firstName,
                lastName: doc.lastName,
                email: doc.email,
                username: doc.username,
                selectedRoom: doc.selectedRoom
            };
        });
    },
    async getOne(userid) {
        let response = await Service.get(`/api/users/${userid}`)
        return response.data.map(doc => {
            return {
                id: doc._id,
                username: doc.username,
                firstName: doc.firstName,
                lastName: doc.lastName,
                chatRooms: doc.chatRooms,
                selectedRoom: doc.selectedRoom
            };
        });
    },
    
    async updateUserField(user, field, value) {
        let response = await Service.post('/api/updateUserField', {
            user: user,
            field: field,
            value: value
        })
        return response
    }
}

export { Service, Rooms, Messages, Users, Camunda, Auth }