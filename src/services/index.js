import axios from 'axios'

let Service = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 1000
})

let Rooms = {
    async getAll(){
        let response = await Service.get('/api/getRooms')
        return response.data.map(doc => {
            return {
                id: doc._id,
                url: doc.source
            };
        });
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

export { Service, Rooms, Users, Files }