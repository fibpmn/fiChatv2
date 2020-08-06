import axios from 'axios'

let Service = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 1000
})

let Rooms = {
    getAll(){
        return Service.get('/api/getRooms')
    }
    /*
    async getAll(){
        let response = await Service.get('/api/getRooms)
        let data = response.data
        data = data.map(doc => {
            return {
                id: doc.id,
                url: doc.source
                itd itd
            };
        });
        return data
    }
    */
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