#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "turtle_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__turtle_interfaces__srv__ShapeCommand_Request() -> *const std::ffi::c_void;
}

#[link(name = "turtle_interfaces__rosidl_generator_c")]
extern "C" {
    fn turtle_interfaces__srv__ShapeCommand_Request__init(msg: *mut ShapeCommand_Request) -> bool;
    fn turtle_interfaces__srv__ShapeCommand_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ShapeCommand_Request>, size: usize) -> bool;
    fn turtle_interfaces__srv__ShapeCommand_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ShapeCommand_Request>);
    fn turtle_interfaces__srv__ShapeCommand_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ShapeCommand_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ShapeCommand_Request>) -> bool;
}

// Corresponds to turtle_interfaces__srv__ShapeCommand_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ShapeCommand_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub command: rosidl_runtime_rs::String,

}



impl Default for ShapeCommand_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !turtle_interfaces__srv__ShapeCommand_Request__init(&mut msg as *mut _) {
        panic!("Call to turtle_interfaces__srv__ShapeCommand_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ShapeCommand_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { turtle_interfaces__srv__ShapeCommand_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { turtle_interfaces__srv__ShapeCommand_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { turtle_interfaces__srv__ShapeCommand_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ShapeCommand_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ShapeCommand_Request where Self: Sized {
  const TYPE_NAME: &'static str = "turtle_interfaces/srv/ShapeCommand_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__turtle_interfaces__srv__ShapeCommand_Request() }
  }
}


#[link(name = "turtle_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__turtle_interfaces__srv__ShapeCommand_Response() -> *const std::ffi::c_void;
}

#[link(name = "turtle_interfaces__rosidl_generator_c")]
extern "C" {
    fn turtle_interfaces__srv__ShapeCommand_Response__init(msg: *mut ShapeCommand_Response) -> bool;
    fn turtle_interfaces__srv__ShapeCommand_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ShapeCommand_Response>, size: usize) -> bool;
    fn turtle_interfaces__srv__ShapeCommand_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ShapeCommand_Response>);
    fn turtle_interfaces__srv__ShapeCommand_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ShapeCommand_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ShapeCommand_Response>) -> bool;
}

// Corresponds to turtle_interfaces__srv__ShapeCommand_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ShapeCommand_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for ShapeCommand_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !turtle_interfaces__srv__ShapeCommand_Response__init(&mut msg as *mut _) {
        panic!("Call to turtle_interfaces__srv__ShapeCommand_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ShapeCommand_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { turtle_interfaces__srv__ShapeCommand_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { turtle_interfaces__srv__ShapeCommand_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { turtle_interfaces__srv__ShapeCommand_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ShapeCommand_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ShapeCommand_Response where Self: Sized {
  const TYPE_NAME: &'static str = "turtle_interfaces/srv/ShapeCommand_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__turtle_interfaces__srv__ShapeCommand_Response() }
  }
}






#[link(name = "turtle_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__turtle_interfaces__srv__ShapeCommand() -> *const std::ffi::c_void;
}

// Corresponds to turtle_interfaces__srv__ShapeCommand
#[allow(missing_docs, non_camel_case_types)]
pub struct ShapeCommand;

impl rosidl_runtime_rs::Service for ShapeCommand {
    type Request = ShapeCommand_Request;
    type Response = ShapeCommand_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__turtle_interfaces__srv__ShapeCommand() }
    }
}


