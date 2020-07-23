rooms="[
    {
      roomId: 1,
      roomName: 'Room 1',
      lastMessage: {
        content: 'Last message received',
        sender_id: 1234,
        username: 'John Doe',
        timestamp: '10:20',
        date: 123242424,
        seen: false,
        new: true
      },
      users: [
        {
          _id: 1234,
          username: 'John Doe',
          status: {
            state: 'online',
            last_changed: 'today, 14:30'
          }
        },
        {
          _id: 4321,
          username: 'John Snow',
          status: {
            state: 'offline',
            last_changed: '14 July, 20:00'
          }
        }
      ],
      typingUsers: [ 4321 ]
    }
  ]"