package service_mapper

import (
	"context"
	"net"

	"google.golang.org/grpc"
	pb "opt/axentx/surrogate-1/service_mapper/proto"
)

// grpcServer implements the protobuf service.
type grpcServer struct {
	pb.UnimplementedMapperServer
}

// GetByRequestID implements the RPC.
func (s *grpcServer) GetByRequestID(ctx context.Context, req *pb.RequestID) (*pb.UpstreamInfo, error) {
	if info, ok := Get(req.Id); ok {
		return &pb.UpstreamInfo{
			ServiceName: info.ServiceName,
			Endpoint:    info.Endpoint,
		}, nil
	}
	// Not found → return empty fields (Node will treat as missing)
	return &pb.UpstreamInfo{}, nil
}

// StartGRPC launches the mapper on a Unix domain socket (fast, no port conflict).
func StartGRPC(socketPath string) error {
	lis, err := net.Listen("unix", socketPath)
	if err != nil {
		return err
	}
	s := grpc.NewServer()
	pb.RegisterMapperServer(s, &grpcServer{})
	return s.Serve(lis)
}