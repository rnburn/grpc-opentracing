/**
 * A OpenTraced server for a go service that implements the store interface.
 */
package main

import (
	"log"
	"net"

	pb "../store"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

const (
	port = ":50051"
)

// server is used to implement helloworld.StoreServer.
type server struct{}

// SayQuantity implements helloworld.StoreServer
func (s *server) GetQuantity(ctx context.Context, in *pb.QuantityRequest) (*pb.QuantityResponse, error) {
	return &pb.QuantityResponse{300}, nil
}

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterStoreServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
