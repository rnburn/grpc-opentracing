/**
 * A OpenTraced server for a go service that implements the store interface.
 */
package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"

	pb "../store"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	"github.com/grpc-ecosystem/grpc-opentracing/go/otgrpc"
	"github.com/lightstep/lightstep-tracer-go"
	"github.com/opentracing/opentracing-go"
)

const (
	port = ":50051"
)

var accessToken = flag.String("access_token", "", "your LightStep access token")

// server is used to implement helloworld.StoreServer.
type server struct{}

// SayQuantity implements helloworld.StoreServer
func (s *server) GetQuantity(ctx context.Context, in *pb.QuantityRequest) (*pb.QuantityResponse, error) {
	return &pb.QuantityResponse{300}, nil
}

func main() {
	flag.Parse()
	if len(*accessToken) == 0 {
		fmt.Println("You must specify --access_token")
		os.Exit(1)
	}

	tracerOpts := lightstep.Options{
		AccessToken: *accessToken,
	}
	tracerOpts.Tags = make(opentracing.Tags)
	tracerOpts.Tags["lightstep.component_name"] = "go.store-server"
	tracer := lightstep.NewTracer(tracerOpts)

	// Set up a connection to the server.
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer(grpc.UnaryInterceptor(
		otgrpc.OpenTracingServerInterceptor(tracer)))
	pb.RegisterStoreServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}

	// Force a flush of the tracer
	err = lightstep.FlushLightStepTracer(tracer)
	if err != nil {
		panic(err)
	}
}
