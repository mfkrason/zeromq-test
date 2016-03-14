
#include "server/Server.hpp"

#include <zmq.hpp>

#include <cstring>
#include <iostream>

int Server::main()
{
	zmq::context_t context(1);
	zmq::socket_t socket(context, ZMQ_REP);
	socket.bind("tcp://*:5555");

	while(1)
	{
		zmq::message_t request;

		socket.recv( &request );

		std::cout << "Received request" << std::endl;

		zmq::message_t reply(5);
		memcpy( reply.data(), "World", 5 );
		//socket.send( &reply );
	}

	return 0;
}

