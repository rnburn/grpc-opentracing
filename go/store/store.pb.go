// Code generated by protoc-gen-go.
// source: store.proto
// DO NOT EDIT!

/*
Package store is a generated protocol buffer package.

It is generated from these files:
	store.proto

It has these top-level messages:
	QuantityRequest
	QuantityResponse
*/
package store

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type QuantityRequest struct {
	ItemId int32 `protobuf:"varint,1,opt,name=item_id,json=itemId" json:"item_id,omitempty"`
}

func (m *QuantityRequest) Reset()                    { *m = QuantityRequest{} }
func (m *QuantityRequest) String() string            { return proto.CompactTextString(m) }
func (*QuantityRequest) ProtoMessage()               {}
func (*QuantityRequest) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{0} }

func (m *QuantityRequest) GetItemId() int32 {
	if m != nil {
		return m.ItemId
	}
	return 0
}

type QuantityResponse struct {
	Quantity int32 `protobuf:"varint,1,opt,name=quantity" json:"quantity,omitempty"`
}

func (m *QuantityResponse) Reset()                    { *m = QuantityResponse{} }
func (m *QuantityResponse) String() string            { return proto.CompactTextString(m) }
func (*QuantityResponse) ProtoMessage()               {}
func (*QuantityResponse) Descriptor() ([]byte, []int) { return fileDescriptor0, []int{1} }

func (m *QuantityResponse) GetQuantity() int32 {
	if m != nil {
		return m.Quantity
	}
	return 0
}

func init() {
	proto.RegisterType((*QuantityRequest)(nil), "store.QuantityRequest")
	proto.RegisterType((*QuantityResponse)(nil), "store.QuantityResponse")
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// Client API for Store service

type StoreClient interface {
	GetQuantity(ctx context.Context, in *QuantityRequest, opts ...grpc.CallOption) (*QuantityResponse, error)
}

type storeClient struct {
	cc *grpc.ClientConn
}

func NewStoreClient(cc *grpc.ClientConn) StoreClient {
	return &storeClient{cc}
}

func (c *storeClient) GetQuantity(ctx context.Context, in *QuantityRequest, opts ...grpc.CallOption) (*QuantityResponse, error) {
	out := new(QuantityResponse)
	err := grpc.Invoke(ctx, "/store.Store/GetQuantity", in, out, c.cc, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// Server API for Store service

type StoreServer interface {
	GetQuantity(context.Context, *QuantityRequest) (*QuantityResponse, error)
}

func RegisterStoreServer(s *grpc.Server, srv StoreServer) {
	s.RegisterService(&_Store_serviceDesc, srv)
}

func _Store_GetQuantity_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(QuantityRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(StoreServer).GetQuantity(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/store.Store/GetQuantity",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(StoreServer).GetQuantity(ctx, req.(*QuantityRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var _Store_serviceDesc = grpc.ServiceDesc{
	ServiceName: "store.Store",
	HandlerType: (*StoreServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GetQuantity",
			Handler:    _Store_GetQuantity_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "store.proto",
}

func init() { proto.RegisterFile("store.proto", fileDescriptor0) }

var fileDescriptor0 = []byte{
	// 142 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x09, 0x6e, 0x88, 0x02, 0xff, 0xe2, 0xe2, 0x2e, 0x2e, 0xc9, 0x2f,
	0x4a, 0xd5, 0x2b, 0x28, 0xca, 0x2f, 0xc9, 0x17, 0x62, 0x05, 0x73, 0x94, 0xb4, 0xb8, 0xf8, 0x03,
	0x4b, 0x13, 0xf3, 0x4a, 0x32, 0x4b, 0x2a, 0x83, 0x52, 0x0b, 0x4b, 0x53, 0x8b, 0x4b, 0x84, 0xc4,
	0xb9, 0xd8, 0x33, 0x4b, 0x52, 0x73, 0xe3, 0x33, 0x53, 0x24, 0x18, 0x15, 0x18, 0x35, 0x58, 0x83,
	0xd8, 0x40, 0x5c, 0xcf, 0x14, 0x25, 0x3d, 0x2e, 0x01, 0x84, 0xda, 0xe2, 0x82, 0xfc, 0xbc, 0xe2,
	0x54, 0x21, 0x29, 0x2e, 0x8e, 0x42, 0xa8, 0x18, 0x54, 0x35, 0x9c, 0x6f, 0xe4, 0xc9, 0xc5, 0x1a,
	0x0c, 0xb2, 0x44, 0xc8, 0x81, 0x8b, 0xdb, 0x3d, 0xb5, 0x04, 0xa6, 0x57, 0x48, 0x4c, 0x0f, 0xe2,
	0x10, 0x34, 0x8b, 0xa5, 0xc4, 0x31, 0xc4, 0x21, 0x96, 0x28, 0x31, 0x24, 0xb1, 0x81, 0x1d, 0x6d,
	0x0c, 0x08, 0x00, 0x00, 0xff, 0xff, 0xf9, 0xfd, 0x40, 0x1d, 0xc3, 0x00, 0x00, 0x00,
}
