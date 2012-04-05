/* Olethros */
/* extern "C" void olethros(tModInfo modInfo[10]); */

/* C-Drivers Callbacks */
/*
extern "C" void DriverInit(tModInfo *modInfo, tRobotItf *robItf);
extern "C" GfParmHandle *DriverNewTrack(tRobotItf *itf, tTrack *track, tSituation *situ);
extern "C" void DriverNewRace(tRobotItf *itf, tCarElt* car, tSituation *s);
extern "C" void DriverDrive(tRobotItf *itf, tCarElt* car, tSituation *s);
extern "C" void DriverPitCmd(tRobotItf *itf, tCarElt* car, tSituation *s);
extern "C" void DriverEndRace(tRobotItf *itf, tCarElt *car, tSituation *s);
extern "C" void DriverShutdown(tRobotItf *itf);
*/

/* SimuV2 */
extern "C" void simuv2(tModInfo *modInfo);
extern "C" void simuv2Init(tSimItf *simItf);
extern "C" void SimConfig(tCarElt *carElt);
extern "C" void SimReConfig(tCarElt *carElt);
extern "C" void SimUpdate(tSituation *situ, double deltaTime, int telemetry);
extern "C" void SimInit(int nbcars);
extern "C" void SimShutdown();

/* Track */
/*
extern "C" void track(tModInfo *modInfo);
extern "C" void trackInit(tTrackItf *ptf, int index);
extern "C" tTrack *trkBuild(tTrackItf *ptf, const char *filename);
extern "C" tTrack *trkBuildEx(tTrackItf *ptf, const char *filename);
extern "C" float trkHeightG(tTrackItf *ptf, tTrackSeg *t, float a, float b);
extern "C" float trkHeightL(tTrackItf *ptf, tTrkLocPos*lp);
extern "C" void trkGlobal2Local(tTrackItf *ptf, tTrackSeg* seg, float X, float Y, tTrkLocPos* pos, int sides);
extern "C" void trkLocal2Global(tTrackItf *ptf, tTrkLocPos*lp, float *a, float *b);
extern "C" void trkSideNormal(tTrackItf *ptf, tTrackSeg*seg, float X, float Y, int i, float v[3]);
extern "C" void trkSurfaceNormal(tTrackItf *ptf, tTrkLocPos *lp, float v[3]);
extern "C" void trkShutdown(tTrackItf *ptf);
*/

/* A dummy structure for pointers on GfParm */
struct tGfParmHandle { void *Dummy; };

/* GfParm */
class tGfParm {
    public:
    GfParmHandle *Handle;
    tGfParm();
    tGfParm(GfParmHandle *handle);
    void ReadFile(char *file, int mode);
    int WriteFile(const char *file, char *name);
    char *GetName();
    char *GetFileName();
    void SetDTD (char *dtd, char*header);
    char *GetStr(char *path, char *key, char *deflt);
    char *GetCurStr(char *path, char *key, char *deflt);
    int SetStr(char *path, char *key, char *val);
    int SetCurStr(char *path, char *key, char *val);
    float GetNum(char *path, char *key, char *unit, float deflt);
    float GetCurNum(char *path, char *key, char *unit, float deflt);
    int SetNum(char *path, char *key, char *unit, float val);
    int SetCurNum(char *path, char *key, char *unit, float val);
    void Clean();
    void ReleaseHandle();
    float Unit2SI(char *unit, float val);
    float SI2Unit(char *unit, float val);
    // int GfParmCheckHandle(void *ref, void *tgt);
    static GfParmHandle *MergeHandles(GfParmHandle *ref, GfParmHandle *tgt, int mode);
    int GetNumBoundaries(char *path, char *key, float *min, float *max);
    int GetEltNb(char *path);
    int ListSeekFirst(char *path);
    int ListSeekNext(char *path);
    char *ListGetCurEltName(char *path);
    int ListClean(char *path);

    enum RMode {
            RMode_STD = 0x01, /**< if handle already openned return it */
            RMode_REREAD = 0x02,  /**< reread the parameters from file and release the previous ones */
            RMode_CREAT = 0x04,   /**< Create the file if doesn't exist */
            RMode_PRIVATE = 0x08
    };
};

#define GFPARM_MMODE_SRC	1 /**< use ref and modify existing parameters with tgt */
#define GFPARM_MMODE_DST	2 /**< use tgt and verify ref parameters */
#define GFPARM_MMODE_RELSRC	4 /**< release ref after the merge */
#define GFPARM_MMODE_RELDST	8 /**< release tgt after the merge */

/* ModInfo */

#ifdef SWIG
typedef int (*tfModPrivInit)(int index, void *);

typedef struct ModInfo {
    char        *name;      /**< name of the module (short) (NULL if no module) */
    char        *desc;      /**< description of the module (can be long) */
    tfModPrivInit fctInit; /**< init function */
    unsigned int    gfId;       /**< supported framework version */
    int         index;      /**< index if multiple interface in one dll */
    int         prio;       /**< priority if needed */
    int         magic;      /**< magic number for integrity check */
} tModInfo;
#endif
