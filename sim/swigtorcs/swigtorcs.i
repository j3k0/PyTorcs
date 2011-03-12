%module TorcsItf
%{
#include "car.h"
/* #include "graphic.h" */
#include "raceman.h"
/* #include "robot.h" */
#include "simu.h"
/* #include "track.h" */
#include "plib/sg.h"
#include "tgf/tgf.h"
#include "swigtorcs.h"
/* #include "robottools/robottools.h" */
%}

%include "typemaps.i"
%include "carrays.i"

%define %cs_array_member(CLASS,TYPE,NAME,PRIVTYPE,PRIVNAME,LENGTH)
%typemap(cscode) CLASS %{
  public PRIVTYPE NAME {
    get { return PRIVTYPE.FromPointer(PRIVNAME);  }
    /* set { PRIVTYPE.frompointer(PRIVNAME).FromArray(LENGTH, value); } */
  }
%}
%enddef

%define %cs_array_member_set_get(CLASS,TYPE,NAME,SETTER,GETTER,LENGTH)
%typemap(cscode) CLASS %{
  public TYPE[] NAME {
    get {
      TYPE[] temp_##NAME = new TYPE[LENGTH];
      for (int i=0; i<LENGTH; ++i) temp_##NAME[i] = GETTER(i);
      return temp_##NAME;
    }
    /* set { for (int i=0; i<LENGTH; ++i) SETTER(i, value[i]); } */
  }
%}
%enddef

/* Ignore all dummy variables */
%ignore Dummy;

/* Math types */
%include swigmath.i
%include swiggfparm.i

%rename(Name) name;
%rename(Desc) desc;
%ignore fctInit;
%rename(GfId) gfId;
%rename(Index) index;
%rename(Priority) prio;
%rename(Magic) magic;
%typemap(cscode) tModInfo %{
  public override string ToString() { return "Module " + Name + " (" + Desc + ")"; }
%}
%include "swigtorcs.h"

%include swigcar.i
/* %include swiggraphic.i */
%include swigraceman.i
/* %include swigrobot.i */
%include swigsimu.i
/* %include swigtrack.i */
/* %include swigrobottools.i */

/* Array definitions */
%define %cs_array_class_root(TYPE,NAME)
  %typemap(cscode) NAME %{
  public TYPE[] AsArray(int arraySize) {
    TYPE[] ret = new TYPE[arraySize];
    for (int i=0; i<arraySize; ++i)
      ret[i] = Get(i);
    return ret;
  }
  public void FromArray(int arraySize, TYPE[] value) {
    for (int i=0; i<arraySize; ++i)
      Set(i, value[i]);
  }
  public TYPE this[int i]  
  {  
      get { return this.Get(i); }  
      set { this.Set(i, value); }
  }  
  %}
  %{
  typedef TYPE NAME;
  %}
  typedef struct NAME {
    /* Put language specific enhancements here */
  } NAME;
  %extend NAME {
    NAME(int nelements) {
      return (TYPE *) calloc(nelements,sizeof(TYPE));
    }
    ~NAME() {
      free(self);
    }
    TYPE GetCopy(int index) {
      return self[index];
    }
    void Set(int index, TYPE value) {
      self[index] = value;
    }
    TYPE * Cast() {
      return self;
    }
    static NAME *FromPointer(TYPE *t) {
      return (NAME *) t;
    }
  };
  %types(NAME = TYPE);
%enddef

%define %cs_array_class_by_copy(TYPE,NAME)
  %extend NAME {
    TYPE Get(int index) {
      return self[index];
    }
  }
  %cs_array_class_root(TYPE,NAME);
%enddef

%define %cs_array_class_by_ref(TYPE,NAME)
  %extend NAME {
    TYPE* Get(int index) {
      return self + index;
    }
  }
  %cs_array_class_root(TYPE,NAME);
%enddef

%cs_array_class_by_copy(float, tFloatArray);
%cs_array_class_by_copy(int, tIntArray);
%cs_array_class_by_ref(t3Dd, t3DdArray);
%cs_array_class_by_ref(tCarElt, tCarEltArray);
%cs_array_class_by_ref(tModInfo, tModInfoArray);
/* %cs_array_class_by_ref(tRobotItf, tRobotItfArray); */
%cs_array_class_by_ref(tWheelSpec, tWheelSpecArray);
%cs_array_class_by_ref(tWheelState, tWheelStateArray);
%cs_array_class_by_ref(tPosd, tPosdArray);

