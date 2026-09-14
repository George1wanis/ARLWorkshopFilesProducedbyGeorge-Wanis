// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from turtle_interfaces:srv/ShapeCommand.idl
// generated code does not contain a copyright notice

#ifndef TURTLE_INTERFACES__SRV__DETAIL__SHAPE_COMMAND__BUILDER_HPP_
#define TURTLE_INTERFACES__SRV__DETAIL__SHAPE_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "turtle_interfaces/srv/detail/shape_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace turtle_interfaces
{

namespace srv
{

namespace builder
{

class Init_ShapeCommand_Request_command
{
public:
  Init_ShapeCommand_Request_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::turtle_interfaces::srv::ShapeCommand_Request command(::turtle_interfaces::srv::ShapeCommand_Request::_command_type arg)
  {
    msg_.command = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtle_interfaces::srv::ShapeCommand_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtle_interfaces::srv::ShapeCommand_Request>()
{
  return turtle_interfaces::srv::builder::Init_ShapeCommand_Request_command();
}

}  // namespace turtle_interfaces


namespace turtle_interfaces
{

namespace srv
{

namespace builder
{

class Init_ShapeCommand_Response_message
{
public:
  explicit Init_ShapeCommand_Response_message(::turtle_interfaces::srv::ShapeCommand_Response & msg)
  : msg_(msg)
  {}
  ::turtle_interfaces::srv::ShapeCommand_Response message(::turtle_interfaces::srv::ShapeCommand_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::turtle_interfaces::srv::ShapeCommand_Response msg_;
};

class Init_ShapeCommand_Response_success
{
public:
  Init_ShapeCommand_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ShapeCommand_Response_message success(::turtle_interfaces::srv::ShapeCommand_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ShapeCommand_Response_message(msg_);
  }

private:
  ::turtle_interfaces::srv::ShapeCommand_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::turtle_interfaces::srv::ShapeCommand_Response>()
{
  return turtle_interfaces::srv::builder::Init_ShapeCommand_Response_success();
}

}  // namespace turtle_interfaces

#endif  // TURTLE_INTERFACES__SRV__DETAIL__SHAPE_COMMAND__BUILDER_HPP_
