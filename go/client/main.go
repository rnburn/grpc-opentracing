package main

import (
	"log"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
	pb "../store"
)

const (
	address     = "localhost:50051"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewStoreClient(conn)

	// Contact the server and print out its response.
  item_id := int32(22)
	r, err := c.GetQuantity(context.Background(), &pb.QuantityRequest{item_id})
	if err != nil {
		log.Fatalf("could not get quantity: %v", err)
	}
	log.Printf("Quantity: %d", r.Quantity)
}
