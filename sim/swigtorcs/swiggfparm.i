/* TODO: Marshall GfParmHandle as GfParm */
%typemap(cstype) GfParmHandle * "tGfParmHandle"
%typemap(csin) GfParmHandle * "tGfParmHandle.getCPtr($csinput)"
%typemap(csout) GfParmHandle * "{
    IntPtr temp = $imcall;
    return new tGfParmHandle(temp, true);
  }"
%typemap(csvarout) GfParmHandle * "
    get {
      return new tGfParmHandle($imcall, false);
    }"
/* %typemap(cstype) GfParmHandle ** "out tGfParmHandle"
   %typemap(csin) GfParmHandle ** "out tGfParmHandle.getCPtr($csinput)" */

%nodefaultctor tGfParmHandle; /* No default/implicit destructor for tGfParmHandle */
%nodefaultdtor tGfParmHandle; /* No default/implicit destructor for tGfParmHandle */

/* %extend tGfParm {
  tGfParm(const char *file, RMode mode) {
    ReadFile(file, (int)mode);
  }
}; */

%typemap(cscode) tGfParm %{
  public tGfParm(string file, RMode mode) : this() {
    ReadFile(file, (int)mode);            
  }
  /* parameters file type */
  public const int PARAMETER = 0; /**< Parameter file */
  public const int TEMPLATE = 1; /**< Template file */
  public const string PARAM_STR = "param";
  public const string TEMPL_STR = "template";

  /* parameters access mode */
  public const int MODIFIABLE = 1;    /**< Parameter file allowed to be modified */
  public const int WRITABLE = 2;  /**< Parameter file allowed to be saved on disk */

  /* parameter file read */
  public enum RMode {
    STD = 0x01, /**< if handle already openned return it */
    REREAD = 0x02,  /**< reread the parameters from file and release the previous ones */
    CREAT = 0x04,   /**< Create the file if doesn't exist */
    PRIVATE = 0x08
  };
%}

%{
/* GfParm */
extern "C" char *GfParmGetStr(GfParmHandle *handle, char *path, char *key, char *deflt);
void tGfParm::ReadFile(char *file, int mode)         { assert(sizeof(tGfParm) == sizeof(void*)); Handle = GfParmReadFile(file, mode); }
int tGfParm::WriteFile(const char *file, char *name) { return GfParmWriteFile(file, Handle, name); }
char *tGfParm::GetName() { return GfParmGetName(Handle); }
char *tGfParm::GetFileName() { return GfParmGetFileName(Handle); }
void tGfParm::SetDTD (char *dtd, char*header) { GfParmSetDTD(Handle, dtd, header); }
char *tGfParm::GetStr(char *path, char *key, char *deflt) { return GfParmGetStr(Handle, path, key, deflt); }
char *tGfParm::GetCurStr(char *path, char *key, char *deflt) { return GfParmGetCurStr(Handle, path, key, deflt); }
int tGfParm::SetStr(char *path, char *key, char *val) { return GfParmSetStr(Handle, path, key, val); }
int tGfParm::SetCurStr(char *path, char *key, char *val) { return GfParmSetCurStr(Handle, path, key, val); }
float tGfParm::GetNum(char *path, char *key, char *unit, float deflt) { return GfParmGetNum(Handle, path, key, unit, deflt); }
float tGfParm::GetCurNum(char *path, char *key, char *unit, float deflt) { return GfParmGetCurNum(Handle, path, key, unit, deflt); }
int tGfParm::SetNum(char *path, char *key, char *unit, float val) { return GfParmSetNum(Handle, path, key, unit, val); }
int tGfParm::SetCurNum(char *path, char *key, char *unit, float val) { return GfParmSetCurNum(Handle, path, key, unit, val); }
void tGfParm::Clean() { GfParmClean(Handle); }
void tGfParm::ReleaseHandle() { GfParmReleaseHandle(Handle); }
float tGfParm::Unit2SI(char *unit, float val) { return GfParmUnit2SI(unit, val); }
float tGfParm::SI2Unit(char *unit, float val) { return GfParmSI2Unit(unit, val); }
int tGfParm::GetNumBoundaries(char *path, char *key, float *min, float *max) { return GfParmGetNumBoundaries(Handle, path, key, min, max); }
int tGfParm::GetEltNb(char *path) { return GfParmGetEltNb(Handle, path); }
int tGfParm::ListSeekFirst(char *path) { return GfParmListSeekFirst(Handle, path); }
int tGfParm::ListSeekNext(char *path) { return GfParmListSeekNext(Handle, path); }
char *tGfParm::ListGetCurEltName(char *path) { return GfParmListGetCurEltName(Handle, path); }
int tGfParm::ListClean(char *path) { return GfParmListClean(Handle, path); }
tGfParm::tGfParm(GfParmHandle *handle) : Handle(handle) {}
tGfParm::tGfParm() : Handle(NULL) {}
GfParmHandle *tGfParm::MergeHandles(GfParmHandle *ref, GfParmHandle *tgt, int mode) { return GfParmMergeHandles(ref, tgt, mode); }
%}
