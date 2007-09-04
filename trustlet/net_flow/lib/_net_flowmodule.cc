#include "Python.h"

#include <glib.h>
#include "net_flow.hh"

extern "C" {
  void init_net_flow();
}

void _net_flow_free(void * p)
{
  net_flow_free((NetFlow *) p);
}

static PyObject* new_flowobj(PyObject * self, PyObject * args)
{
  // no args.
  if (!PyArg_ParseTuple(args, "")) {
    return NULL;
  }

  NetFlow * flow = net_flow_new();

  return PyCObject_FromVoidPtr(flow, _net_flow_free); // @CTB
}

static PyObject * add_edge(PyObject * self, PyObject * args)
{
  PyObject * flow_o;
  char * from, * to;

  if (!PyArg_ParseTuple(args, "Oss", &flow_o, &from, &to)) {
    return NULL;
  }

  NetFlow * flow = (NetFlow *) PyCObject_AsVoidPtr(flow_o);

  net_flow_add_edge(flow, from, to);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject * calc_max_flow(PyObject * self, PyObject * args)
{
  PyObject * flow_o, * capacities_o;
  char * seed_name;

  if (!PyArg_ParseTuple(args, "OsO", &flow_o, &seed_name, &capacities_o)) {
    return NULL;
  }

  if (!PyList_Check(capacities_o)) { return NULL; }

  int n_capacities = PyList_Size(capacities_o);
  int capacities[n_capacities];
  for (int i = 0; i < n_capacities; i++) {
    PyObject * capacity_o = PyList_GetItem(capacities_o, i);

    int capacity = (int) PyInt_AsLong(capacity_o);
    capacities[i] = capacity;
  }

  NetFlow * flow = (NetFlow *) PyCObject_AsVoidPtr(flow_o);

  int seed_n = net_flow_find_node(flow, seed_name);

  net_flow_max_flow(flow, seed_n, &capacities[0], n_capacities);

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject * extract(PyObject * self, PyObject * args)
{
  PyObject * flow_o;
  int n_nodes;

  if (!PyArg_ParseTuple(args, "Oi", &flow_o, &n_nodes)) {
    return NULL;
  }

  NetFlow * flow = (NetFlow *) PyCObject_AsVoidPtr(flow_o);
  int * result = net_flow_extract(flow);

  PyObject * result_o = PyList_New(n_nodes);
  for (int i = 0; i < n_nodes; i++) {
    PyList_SET_ITEM(result_o, i, PyInt_FromLong(result[i]));
  }

  g_free(result);

  return result_o;
}

static PyMethodDef NetFlowMethods[] = {
  { "new_flowobj", new_flowobj, METH_VARARGS, "create a new trust network" },
  { "add_edge", add_edge, METH_VARARGS, "add an edge to the trust network" },
  { "calc_max_flow", calc_max_flow, METH_VARARGS, "calculate the network flow" },
  { "extract", extract, METH_VARARGS, "extract node trust information" },
  { NULL, NULL, 0, NULL }
};

DL_EXPORT(void) init_net_flow(void)
{
  PyObject * m;
  m = Py_InitModule("_net_flow", NetFlowMethods);
}
