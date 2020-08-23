import axios from 'axios'

let Service = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 10000
})

let Rooms = {
    async getAll(){
        let response = await Service.get('/api/getRooms')
        return response.data.map(doc => {
            return {
                id: doc._id,
                name: doc.name,
                users: doc.users,
                messages: doc.messages
            };
        });
    }
}

let Messages = {
    async getForRoom(){
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
    }
}
let Users = {
    getAll(){
        return Service.get('/api/getUsers')
    }
}

let Files = {
    getAll(){
        return Service.get('/api/getFiles')
    }
}

export { Service, Rooms, Messages, Users, Files }