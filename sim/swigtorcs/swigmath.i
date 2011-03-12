typedef float sgVec2 [2];
typedef float sgVec3 [3];
typedef float sgVec4 [4];
typedef sgVec4 sgQuat;
typedef float sgMat3 [9];
typedef float sgMat4 [16];

typedef float tdble;
typedef int int32_t;
typedef unsigned int uint32_t;

%rename(X) x;
%rename(Y) y;
%rename(Z) z;
%rename(AX) ax;
%rename(AY) ay;
%rename(AZ) az;
%rename(Position) pos;
%rename(Velocity) vel;
%rename(Acceleration) acc;

typedef struct { float   x,y,z; } t3Df;
typedef struct { tdble   x,y,z; } t3Dd;
typedef struct { int     x,y,z; } t3Di;
typedef struct { tdble   x,y,z,ax,ay,az; } tPosd;
%extend tPosd { tdble Roll, Pitch, Yaw; };
typedef struct { tPosd pos; tPosd vel; tPosd acc; } tDynPt;
typedef struct { t3Dd F; t3Dd M; } tForces;

/* sgMat4 */
%typemap(cstype) sgMat4 "Math3D.Matrix4"
%typemap(csvarout) sgMat4 "
    get {
      IntPtr temp = $imcall;
      tFloatArray m = new tFloatArray(temp, false);
      return new Math3D.Matrix4(m.GetCopy(0), m.GetCopy(4), m.GetCopy( 8), m.GetCopy(12),
                                m.GetCopy(1), m.GetCopy(5), m.GetCopy( 9), m.GetCopy(13),
                                m.GetCopy(2), m.GetCopy(6), m.GetCopy(10), m.GetCopy(14),
                                m.GetCopy(3), m.GetCopy(7), m.GetCopy(11), m.GetCopy(15));
    }"
/* XXX Setter is not possible (see OgreDotNet and others...) needs custom methods to set matrices */

%{
/* tPosd */
tdble tPosd_Roll_get(tPosd *p) { return p->ax; }
tdble tPosd_Pitch_get(tPosd *p) { return p->ay; }
tdble tPosd_Yaw_get(tPosd *p) { return p->az; }
void tPosd_Roll_set(tPosd *p, tdble v) { p->ax = v; }
void tPosd_Pitch_set(tPosd *p, tdble v) { p->ay = v; }
void tPosd_Yaw_set(tPosd *p, tdble v) { p->az = v; }
%}

