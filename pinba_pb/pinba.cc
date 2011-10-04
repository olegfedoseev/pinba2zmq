#include <Python.h>
#include <string>
#include "structmember.h"
#include "pinba.pb.h"



static PyObject *
fastpb_convert5(::google::protobuf::int32 value)
{
    return PyLong_FromLong(value);
}

static PyObject *
fastpb_convert3(::google::protobuf::int64 value)
{
    return PyLong_FromLongLong(value);
}

static PyObject *
fastpb_convert18(::google::protobuf::int64 value)
{
    return PyLong_FromLongLong(value);
}

static PyObject *
fastpb_convert17(::google::protobuf::int32 value)
{
    return PyLong_FromLong(value);
}

static PyObject *
fastpb_convert13(::google::protobuf::uint32 value)
{
    return PyLong_FromUnsignedLong(value);
}

static PyObject *
fastpb_convert4(::google::protobuf::uint64 value)
{
    return PyLong_FromUnsignedLong(value);
}

static PyObject *
fastpb_convert1(double value)
{
    return PyFloat_FromDouble(value);
}

static PyObject *
fastpb_convert2(float value)
{
   return PyFloat_FromDouble(value);
}

static PyObject *
fastpb_convert9(const ::std::string &value)
{
    return PyUnicode_Decode(value.data(), value.length(), "utf-8", NULL);
}

static PyObject *
fastpb_convert12(const ::std::string &value)
{
    return PyString_FromStringAndSize(value.data(), value.length());
}

static PyObject *
fastpb_convert8(bool value)
{
    return PyBool_FromLong(value ? 1 : 0);
}

static PyObject *
fastpb_convert14(int value)
{
    // TODO(robbyw): Check EnumName_IsValid(value)
    return PyLong_FromLong(value);
}




  typedef struct {
      PyObject_HEAD

      Pinba::Request *protobuf;
  } Request;

  static void
  Request_dealloc(Request* self)
  {
      self->ob_type->tp_free((PyObject*)self);

      delete self->protobuf;
  }

  static PyObject *
  Request_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
  {
      Request *self;

      self = (Request *)type->tp_alloc(type, 0);

      self->protobuf = new Pinba::Request();

      return (PyObject *)self;
  }

  static PyObject *
  Request_SerializeToString(Request* self)
  {
      std::string result;
      Py_BEGIN_ALLOW_THREADS
      self->protobuf->SerializeToString(&result);
      Py_END_ALLOW_THREADS
      return PyString_FromStringAndSize(result.data(), result.length());
  }


  static PyObject *
  Request_ParseFromString(Request* self, PyObject *value)
  {
      std::string serialized(PyString_AsString(value), PyString_Size(value));
      Py_BEGIN_ALLOW_THREADS
      self->protobuf->ParseFromString(serialized);
      Py_END_ALLOW_THREADS
      Py_RETURN_NONE;
  }


  
    

    static PyObject *
    Request_gethostname(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_hostname()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert9(
                  self->protobuf->hostname());

        
    }

    static int
    Request_sethostname(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_hostname();
        return 0;
      }

      
        PyObject *value = input;
      

      
        // string
        bool reallocated = false;
        if (PyUnicode_Check(value)) {
          value = PyUnicode_AsEncodedString(value, "utf-8", NULL);
          reallocated = true;
        }

        if (! PyString_Check(value)) {
          PyErr_SetString(PyExc_TypeError, "The hostname attribute value must be a string");
          return -1;
        }

        std::string protoValue(PyString_AsString(value), PyString_Size(value));
        if (reallocated) {
          Py_XDECREF(value);
        }

      

      
        
          self->protobuf->set_hostname(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getserver_name(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_server_name()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert9(
                  self->protobuf->server_name());

        
    }

    static int
    Request_setserver_name(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_server_name();
        return 0;
      }

      
        PyObject *value = input;
      

      
        // string
        bool reallocated = false;
        if (PyUnicode_Check(value)) {
          value = PyUnicode_AsEncodedString(value, "utf-8", NULL);
          reallocated = true;
        }

        if (! PyString_Check(value)) {
          PyErr_SetString(PyExc_TypeError, "The server_name attribute value must be a string");
          return -1;
        }

        std::string protoValue(PyString_AsString(value), PyString_Size(value));
        if (reallocated) {
          Py_XDECREF(value);
        }

      

      
        
          self->protobuf->set_server_name(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getscript_name(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_script_name()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert9(
                  self->protobuf->script_name());

        
    }

    static int
    Request_setscript_name(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_script_name();
        return 0;
      }

      
        PyObject *value = input;
      

      
        // string
        bool reallocated = false;
        if (PyUnicode_Check(value)) {
          value = PyUnicode_AsEncodedString(value, "utf-8", NULL);
          reallocated = true;
        }

        if (! PyString_Check(value)) {
          PyErr_SetString(PyExc_TypeError, "The script_name attribute value must be a string");
          return -1;
        }

        std::string protoValue(PyString_AsString(value), PyString_Size(value));
        if (reallocated) {
          Py_XDECREF(value);
        }

      

      
        
          self->protobuf->set_script_name(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getrequest_count(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_request_count()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert13(
                  self->protobuf->request_count());

        
    }

    static int
    Request_setrequest_count(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_request_count();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The request_count attribute value must be an integer");
          return -1;
        }

      

      
        
          self->protobuf->set_request_count(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getdocument_size(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_document_size()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert13(
                  self->protobuf->document_size());

        
    }

    static int
    Request_setdocument_size(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_document_size();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The document_size attribute value must be an integer");
          return -1;
        }

      

      
        
          self->protobuf->set_document_size(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getmemory_peak(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_memory_peak()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert13(
                  self->protobuf->memory_peak());

        
    }

    static int
    Request_setmemory_peak(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_memory_peak();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The memory_peak attribute value must be an integer");
          return -1;
        }

      

      
        
          self->protobuf->set_memory_peak(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getrequest_time(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_request_time()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert2(
                  self->protobuf->request_time());

        
    }

    static int
    Request_setrequest_time(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_request_time();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
        float protoValue;
        
        if (PyFloat_Check(value)) {
          protoValue = PyFloat_AsDouble(value);
        } else if (PyInt_Check(value)) {
          protoValue = PyInt_AsLong(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsLongLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                        
                          "The request_time attribute value must be a float");
                        
          return -1;
        }

      

      
        
          self->protobuf->set_request_time(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getru_utime(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_ru_utime()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert2(
                  self->protobuf->ru_utime());

        
    }

    static int
    Request_setru_utime(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_ru_utime();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
        float protoValue;
        
        if (PyFloat_Check(value)) {
          protoValue = PyFloat_AsDouble(value);
        } else if (PyInt_Check(value)) {
          protoValue = PyInt_AsLong(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsLongLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                        
                          "The ru_utime attribute value must be a float");
                        
          return -1;
        }

      

      
        
          self->protobuf->set_ru_utime(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_getru_stime(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_ru_stime()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert2(
                  self->protobuf->ru_stime());

        
    }

    static int
    Request_setru_stime(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_ru_stime();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
        float protoValue;
        
        if (PyFloat_Check(value)) {
          protoValue = PyFloat_AsDouble(value);
        } else if (PyInt_Check(value)) {
          protoValue = PyInt_AsLong(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsLongLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                        
                          "The ru_stime attribute value must be a float");
                        
          return -1;
        }

      

      
        
          self->protobuf->set_ru_stime(protoValue);
        
      

      return 0;
    }
  
    

    static PyObject *
    Request_gettimer_hit_count(Request *self, void *closure)
    {
        
          int len = self->protobuf->timer_hit_count_size();
          PyObject *tuple = PyTuple_New(len);
          for (int i = 0; i < len; ++i) {
            PyObject *value =
                fastpb_convert13(
                    self->protobuf->timer_hit_count(i));
            PyTuple_SetItem(tuple, i, value);
          }
          return tuple;

        
    }

    static int
    Request_settimer_hit_count(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_timer_hit_count();
        return 0;
      }

      
        if (PyString_Check(input)) {
          PyErr_SetString(PyExc_TypeError, "The timer_hit_count attribute value must be a sequence");
          return -1;
        }
        PyObject *sequence = PySequence_Fast(input, "The timer_hit_count attribute value must be a sequence");
        self->protobuf->clear_timer_hit_count();
        for (Py_ssize_t i = 0, len = PySequence_Length(sequence); i < len; ++i) {
          PyObject *value = PySequence_Fast_GET_ITEM(sequence, i);

      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The timer_hit_count attribute value must be an integer");
          return -1;
        }

      

      
          
            self->protobuf->add_timer_hit_count(protoValue);
          
        }

        Py_XDECREF(sequence);
      

      return 0;
    }
  
    

    static PyObject *
    Request_gettimer_value(Request *self, void *closure)
    {
        
          int len = self->protobuf->timer_value_size();
          PyObject *tuple = PyTuple_New(len);
          for (int i = 0; i < len; ++i) {
            PyObject *value =
                fastpb_convert2(
                    self->protobuf->timer_value(i));
            PyTuple_SetItem(tuple, i, value);
          }
          return tuple;

        
    }

    static int
    Request_settimer_value(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_timer_value();
        return 0;
      }

      
        if (PyString_Check(input)) {
          PyErr_SetString(PyExc_TypeError, "The timer_value attribute value must be a sequence");
          return -1;
        }
        PyObject *sequence = PySequence_Fast(input, "The timer_value attribute value must be a sequence");
        self->protobuf->clear_timer_value();
        for (Py_ssize_t i = 0, len = PySequence_Length(sequence); i < len; ++i) {
          PyObject *value = PySequence_Fast_GET_ITEM(sequence, i);

      

      
        
        float protoValue;
        
        if (PyFloat_Check(value)) {
          protoValue = PyFloat_AsDouble(value);
        } else if (PyInt_Check(value)) {
          protoValue = PyInt_AsLong(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsLongLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                        
                          "The timer_value attribute value must be a float");
                        
          return -1;
        }

      

      
          
            self->protobuf->add_timer_value(protoValue);
          
        }

        Py_XDECREF(sequence);
      

      return 0;
    }
  
    

    static PyObject *
    Request_gettimer_tag_count(Request *self, void *closure)
    {
        
          int len = self->protobuf->timer_tag_count_size();
          PyObject *tuple = PyTuple_New(len);
          for (int i = 0; i < len; ++i) {
            PyObject *value =
                fastpb_convert13(
                    self->protobuf->timer_tag_count(i));
            PyTuple_SetItem(tuple, i, value);
          }
          return tuple;

        
    }

    static int
    Request_settimer_tag_count(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_timer_tag_count();
        return 0;
      }

      
        if (PyString_Check(input)) {
          PyErr_SetString(PyExc_TypeError, "The timer_tag_count attribute value must be a sequence");
          return -1;
        }
        PyObject *sequence = PySequence_Fast(input, "The timer_tag_count attribute value must be a sequence");
        self->protobuf->clear_timer_tag_count();
        for (Py_ssize_t i = 0, len = PySequence_Length(sequence); i < len; ++i) {
          PyObject *value = PySequence_Fast_GET_ITEM(sequence, i);

      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The timer_tag_count attribute value must be an integer");
          return -1;
        }

      

      
          
            self->protobuf->add_timer_tag_count(protoValue);
          
        }

        Py_XDECREF(sequence);
      

      return 0;
    }
  
    

    static PyObject *
    Request_gettimer_tag_name(Request *self, void *closure)
    {
        
          int len = self->protobuf->timer_tag_name_size();
          PyObject *tuple = PyTuple_New(len);
          for (int i = 0; i < len; ++i) {
            PyObject *value =
                fastpb_convert13(
                    self->protobuf->timer_tag_name(i));
            PyTuple_SetItem(tuple, i, value);
          }
          return tuple;

        
    }

    static int
    Request_settimer_tag_name(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_timer_tag_name();
        return 0;
      }

      
        if (PyString_Check(input)) {
          PyErr_SetString(PyExc_TypeError, "The timer_tag_name attribute value must be a sequence");
          return -1;
        }
        PyObject *sequence = PySequence_Fast(input, "The timer_tag_name attribute value must be a sequence");
        self->protobuf->clear_timer_tag_name();
        for (Py_ssize_t i = 0, len = PySequence_Length(sequence); i < len; ++i) {
          PyObject *value = PySequence_Fast_GET_ITEM(sequence, i);

      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The timer_tag_name attribute value must be an integer");
          return -1;
        }

      

      
          
            self->protobuf->add_timer_tag_name(protoValue);
          
        }

        Py_XDECREF(sequence);
      

      return 0;
    }
  
    

    static PyObject *
    Request_gettimer_tag_value(Request *self, void *closure)
    {
        
          int len = self->protobuf->timer_tag_value_size();
          PyObject *tuple = PyTuple_New(len);
          for (int i = 0; i < len; ++i) {
            PyObject *value =
                fastpb_convert13(
                    self->protobuf->timer_tag_value(i));
            PyTuple_SetItem(tuple, i, value);
          }
          return tuple;

        
    }

    static int
    Request_settimer_tag_value(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_timer_tag_value();
        return 0;
      }

      
        if (PyString_Check(input)) {
          PyErr_SetString(PyExc_TypeError, "The timer_tag_value attribute value must be a sequence");
          return -1;
        }
        PyObject *sequence = PySequence_Fast(input, "The timer_tag_value attribute value must be a sequence");
        self->protobuf->clear_timer_tag_value();
        for (Py_ssize_t i = 0, len = PySequence_Length(sequence); i < len; ++i) {
          PyObject *value = PySequence_Fast_GET_ITEM(sequence, i);

      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The timer_tag_value attribute value must be an integer");
          return -1;
        }

      

      
          
            self->protobuf->add_timer_tag_value(protoValue);
          
        }

        Py_XDECREF(sequence);
      

      return 0;
    }
  
    

    static PyObject *
    Request_getdictionary(Request *self, void *closure)
    {
        
          int len = self->protobuf->dictionary_size();
          PyObject *tuple = PyTuple_New(len);
          for (int i = 0; i < len; ++i) {
            PyObject *value =
                fastpb_convert9(
                    self->protobuf->dictionary(i));
            PyTuple_SetItem(tuple, i, value);
          }
          return tuple;

        
    }

    static int
    Request_setdictionary(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_dictionary();
        return 0;
      }

      
        if (PyString_Check(input)) {
          PyErr_SetString(PyExc_TypeError, "The dictionary attribute value must be a sequence");
          return -1;
        }
        PyObject *sequence = PySequence_Fast(input, "The dictionary attribute value must be a sequence");
        self->protobuf->clear_dictionary();
        for (Py_ssize_t i = 0, len = PySequence_Length(sequence); i < len; ++i) {
          PyObject *value = PySequence_Fast_GET_ITEM(sequence, i);

      

      
        // string
        bool reallocated = false;
        if (PyUnicode_Check(value)) {
          value = PyUnicode_AsEncodedString(value, "utf-8", NULL);
          reallocated = true;
        }

        if (! PyString_Check(value)) {
          PyErr_SetString(PyExc_TypeError, "The dictionary attribute value must be a string");
          return -1;
        }

        std::string protoValue(PyString_AsString(value), PyString_Size(value));
        if (reallocated) {
          Py_XDECREF(value);
        }

      

      
          
            self->protobuf->add_dictionary(protoValue);
          
        }

        Py_XDECREF(sequence);
      

      return 0;
    }
  
    

    static PyObject *
    Request_getstatus(Request *self, void *closure)
    {
        
          if (! self->protobuf->has_status()) {
            Py_RETURN_NONE;
          }

          return
              fastpb_convert13(
                  self->protobuf->status());

        
    }

    static int
    Request_setstatus(Request *self, PyObject *input, void *closure)
    {
      if (input == NULL || input == Py_None) {
        self->protobuf->clear_status();
        return 0;
      }

      
        PyObject *value = input;
      

      
        
          ::google::protobuf::uint32 protoValue;
        

        // uint32
        if (PyInt_Check(value)) {
          protoValue = PyInt_AsUnsignedLongMask(value);
        } else if (PyLong_Check(value)) {
          protoValue = PyLong_AsUnsignedLong(value);
        } else {
          PyErr_SetString(PyExc_TypeError,
                          "The status attribute value must be an integer");
          return -1;
        }

      

      
        
          self->protobuf->set_status(protoValue);
        
      

      return 0;
    }
  

  static int
  Request_init(Request *self, PyObject *args, PyObject *kwds)
  {
      
        
          PyObject *hostname = NULL;
        
          PyObject *server_name = NULL;
        
          PyObject *script_name = NULL;
        
          PyObject *request_count = NULL;
        
          PyObject *document_size = NULL;
        
          PyObject *memory_peak = NULL;
        
          PyObject *request_time = NULL;
        
          PyObject *ru_utime = NULL;
        
          PyObject *ru_stime = NULL;
        
          PyObject *timer_hit_count = NULL;
        
          PyObject *timer_value = NULL;
        
          PyObject *timer_tag_count = NULL;
        
          PyObject *timer_tag_name = NULL;
        
          PyObject *timer_tag_value = NULL;
        
          PyObject *dictionary = NULL;
        
          PyObject *status = NULL;
        

        static char *kwlist[] = {
          
            (char *) "hostname",
          
            (char *) "server_name",
          
            (char *) "script_name",
          
            (char *) "request_count",
          
            (char *) "document_size",
          
            (char *) "memory_peak",
          
            (char *) "request_time",
          
            (char *) "ru_utime",
          
            (char *) "ru_stime",
          
            (char *) "timer_hit_count",
          
            (char *) "timer_value",
          
            (char *) "timer_tag_count",
          
            (char *) "timer_tag_name",
          
            (char *) "timer_tag_value",
          
            (char *) "dictionary",
          
            (char *) "status",
          
          NULL
        };

        if (! PyArg_ParseTupleAndKeywords(
            args, kwds, "|OOOOOOOOOOOOOOOO", kwlist,
            &hostname,&server_name,&script_name,&request_count,&document_size,&memory_peak,&request_time,&ru_utime,&ru_stime,&timer_hit_count,&timer_value,&timer_tag_count,&timer_tag_name,&timer_tag_value,&dictionary,&status))
          return -1;

        
          if (hostname) {
            if (Request_sethostname(self, hostname, NULL) < 0) {
              return -1;
            }
          }
        
          if (server_name) {
            if (Request_setserver_name(self, server_name, NULL) < 0) {
              return -1;
            }
          }
        
          if (script_name) {
            if (Request_setscript_name(self, script_name, NULL) < 0) {
              return -1;
            }
          }
        
          if (request_count) {
            if (Request_setrequest_count(self, request_count, NULL) < 0) {
              return -1;
            }
          }
        
          if (document_size) {
            if (Request_setdocument_size(self, document_size, NULL) < 0) {
              return -1;
            }
          }
        
          if (memory_peak) {
            if (Request_setmemory_peak(self, memory_peak, NULL) < 0) {
              return -1;
            }
          }
        
          if (request_time) {
            if (Request_setrequest_time(self, request_time, NULL) < 0) {
              return -1;
            }
          }
        
          if (ru_utime) {
            if (Request_setru_utime(self, ru_utime, NULL) < 0) {
              return -1;
            }
          }
        
          if (ru_stime) {
            if (Request_setru_stime(self, ru_stime, NULL) < 0) {
              return -1;
            }
          }
        
          if (timer_hit_count) {
            if (Request_settimer_hit_count(self, timer_hit_count, NULL) < 0) {
              return -1;
            }
          }
        
          if (timer_value) {
            if (Request_settimer_value(self, timer_value, NULL) < 0) {
              return -1;
            }
          }
        
          if (timer_tag_count) {
            if (Request_settimer_tag_count(self, timer_tag_count, NULL) < 0) {
              return -1;
            }
          }
        
          if (timer_tag_name) {
            if (Request_settimer_tag_name(self, timer_tag_name, NULL) < 0) {
              return -1;
            }
          }
        
          if (timer_tag_value) {
            if (Request_settimer_tag_value(self, timer_tag_value, NULL) < 0) {
              return -1;
            }
          }
        
          if (dictionary) {
            if (Request_setdictionary(self, dictionary, NULL) < 0) {
              return -1;
            }
          }
        
          if (status) {
            if (Request_setstatus(self, status, NULL) < 0) {
              return -1;
            }
          }
        
      

      return 0;
  }

  static PyMemberDef Request_members[] = {
      {NULL}  // Sentinel
  };


  static PyGetSetDef Request_getsetters[] = {
    
      {(char *)"hostname",
       (getter)Request_gethostname, (setter)Request_sethostname,
       (char *)"",
       NULL},
    
      {(char *)"server_name",
       (getter)Request_getserver_name, (setter)Request_setserver_name,
       (char *)"",
       NULL},
    
      {(char *)"script_name",
       (getter)Request_getscript_name, (setter)Request_setscript_name,
       (char *)"",
       NULL},
    
      {(char *)"request_count",
       (getter)Request_getrequest_count, (setter)Request_setrequest_count,
       (char *)"",
       NULL},
    
      {(char *)"document_size",
       (getter)Request_getdocument_size, (setter)Request_setdocument_size,
       (char *)"",
       NULL},
    
      {(char *)"memory_peak",
       (getter)Request_getmemory_peak, (setter)Request_setmemory_peak,
       (char *)"",
       NULL},
    
      {(char *)"request_time",
       (getter)Request_getrequest_time, (setter)Request_setrequest_time,
       (char *)"",
       NULL},
    
      {(char *)"ru_utime",
       (getter)Request_getru_utime, (setter)Request_setru_utime,
       (char *)"",
       NULL},
    
      {(char *)"ru_stime",
       (getter)Request_getru_stime, (setter)Request_setru_stime,
       (char *)"",
       NULL},
    
      {(char *)"timer_hit_count",
       (getter)Request_gettimer_hit_count, (setter)Request_settimer_hit_count,
       (char *)"",
       NULL},
    
      {(char *)"timer_value",
       (getter)Request_gettimer_value, (setter)Request_settimer_value,
       (char *)"",
       NULL},
    
      {(char *)"timer_tag_count",
       (getter)Request_gettimer_tag_count, (setter)Request_settimer_tag_count,
       (char *)"",
       NULL},
    
      {(char *)"timer_tag_name",
       (getter)Request_gettimer_tag_name, (setter)Request_settimer_tag_name,
       (char *)"",
       NULL},
    
      {(char *)"timer_tag_value",
       (getter)Request_gettimer_tag_value, (setter)Request_settimer_tag_value,
       (char *)"",
       NULL},
    
      {(char *)"dictionary",
       (getter)Request_getdictionary, (setter)Request_setdictionary,
       (char *)"",
       NULL},
    
      {(char *)"status",
       (getter)Request_getstatus, (setter)Request_setstatus,
       (char *)"",
       NULL},
    
      {NULL}  // Sentinel
  };


  static PyMethodDef Request_methods[] = {
      {"SerializeToString", (PyCFunction)Request_SerializeToString, METH_NOARGS,
       "Serializes the protocol buffer to a string."
      },
      {"ParseFromString", (PyCFunction)Request_ParseFromString, METH_O,
       "Parses the protocol buffer from a string."
      },
      {NULL}  // Sentinel
  };


  static PyTypeObject RequestType = {
      PyObject_HEAD_INIT(NULL)
      0,                                      /*ob_size*/
      "Pinba.Request",  /*tp_name*/
      sizeof(Request),             /*tp_basicsize*/
      0,                                      /*tp_itemsize*/
      (destructor)Request_dealloc, /*tp_dealloc*/
      0,                                      /*tp_print*/
      0,                                      /*tp_getattr*/
      0,                                      /*tp_setattr*/
      0,                                      /*tp_compare*/
      0,                                      /*tp_repr*/
      0,                                      /*tp_as_number*/
      0,                                      /*tp_as_sequence*/
      0,                                      /*tp_as_mapping*/
      0,                                      /*tp_hash */
      0,                                      /*tp_call*/
      0,                                      /*tp_str*/
      0,                                      /*tp_getattro*/
      0,                                      /*tp_setattro*/
      0,                                      /*tp_as_buffer*/
      Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
      "Request objects",           /* tp_doc */
      0,                                      /* tp_traverse */
      0,                                      /* tp_clear */
      0,                   	 	                /* tp_richcompare */
      0,	   	                                /* tp_weaklistoffset */
      0,                   		                /* tp_iter */
      0,		                                  /* tp_iternext */
      Request_methods,             /* tp_methods */
      Request_members,             /* tp_members */
      Request_getsetters,          /* tp_getset */
      0,                                      /* tp_base */
      0,                                      /* tp_dict */
      0,                                      /* tp_descr_get */
      0,                                      /* tp_descr_set */
      0,                                      /* tp_dictoffset */
      (initproc)Request_init,      /* tp_init */
      0,                                      /* tp_alloc */
      Request_new,                 /* tp_new */
  };



static PyMethodDef module_methods[] = {
    {NULL}  // Sentinel
};

#ifndef PyMODINIT_FUNC	// Declarations for DLL import/export.
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initPinba(void)
{
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    PyObject* m;

    

    
      if (PyType_Ready(&RequestType) < 0)
          return;
    

    m = Py_InitModule3("Pinba", module_methods,
                       "");

    if (m == NULL)
      return;

    

    
      Py_INCREF(&RequestType);
      PyModule_AddObject(m, "Request", (PyObject *)&RequestType);
    
}