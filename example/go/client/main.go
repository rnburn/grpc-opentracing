/**
 * A OpenTraced client for a go service that implements the store interface.
 */
package main

import (
	"log"
  "flag"
  "fmt"
  "os"

	pb "../store"
	"golang.org/x/net/context"
	"google.golang.org/grpc"

  "github.com/opentracing/opentracing-go"
  "github.com/lightstep/lightstep-tracer-go"
  "github.com/grpc-ecosystem/grpc-opentracing/go/otgrpc"
)

const (
	address = "localhost:50051"
)

var accessToken = flag.String("access_token", "", "your LightStep access token")

func main() {
  flag.Parse()
  if len(*accessToken) == 0 {
    fmt.Println("You must specify --access_token")
    os.Exit(1)
  }

  // Set up the LightStep tracer
  tracerOpts := lightstep.Options{
    AccessToken : *accessToken,
  }
  tracerOpts.Tags = make(opentracing.Tags)
  tracerOpts.Tags["lightstep.component_name"] = "go.store-client"
  tracer := lightstep.NewTracer(tracerOpts)

	// Set up a connection to the server.
	conn, err := grpc.Dial(
    address, 
    grpc.WithInsecure(),
    grpc.WithUnaryInterceptor(
      otgrpc.OpenTracingClientInterceptor(tracer)))
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

  // Force a flush of the tracer
  err = lightstep.FlushLightStepTracer(tracer)
  if err != nil {
    panic(err)
  }
}
