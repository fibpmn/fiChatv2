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

    //start process instance
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
    async StartProcessInstance(key, name, username) {
        await Service.post(`/api/process-instance/${key}`, { name, username })
    },

    //get user task form
    async getTaskFormVariables(username) {
        let response = await Service.get(`/api/task/${username}`)
        let doc = response.data
        return {
            model: doc.model,
            schema: doc.schema
        }
    },
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

    //malo veca funkcija, ne znam kako bih ju nazvao
    async tonijevafunkcija(user) {
        let response = await Service.get(`/api/task/state/${user}`)
        return response.data;
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
            };
        });
    },

    updateUserField(user, field, value) {
        Service.post('/api/updateUserField', {
            user: user,
            field: field,
            value: value
        })
            .then(
                response => {
                    response;
                },
                error => {
                    console.log(error);
                }
            );
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
        let response = await Service.get(`/api/getLastRoomMessage/${roomid}`)
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
    },
    addMessage(message) {
        Service.post('/api/addMessage',
            {
                room_id: message.room_id,
                content: message.content,
                sender_id: message.sender_id,
                timestamp: message.timestamp,
                seen: message.seen
            })
            .then(
                response => {
                    response;
                },
                error => {
                    console.log(error);
                }
            );

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

export { Service, Rooms, Messages, Users, Camunda, Auth }