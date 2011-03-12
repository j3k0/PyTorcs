/* Array members */
%ignore angle;   /* Ignore tTrackSeg.angle[7]: replaced by AngleZS, AngleZE, [...] */
%ignore vertex;  /* Ignore tTrackSeg.vertex[4]: replaced by VertexSL, VertexSR, [...] */
%ignore barrier; /* Ignore tTrackSeg.barrier[2]: replaced by BarrierR, BarrierL */

/* Function pointers */
%ignore trkBuild;
%ignore trkBuildEx;
%ignore trkHeightG;
%ignore trkHeightL;
%ignore trkGlobal2Local;
%ignore trkLocal2Global;
%ignore trkSideNormal;
%ignore trkSurfaceNormal;
%ignore trkShutdown;

/* Renaming */
%rename(Arc) arc;
%rename(Author) author;
%rename(Background) background;
%rename(Background2) background2;
%rename(BackgroundType) bgtype;
%rename(Camera) cam;
%rename(CarsPerPit) carsPerPit;
%rename(Category) category;
%rename(Center) center;
%rename(DriversPits) driversPits;
%rename(DriversPitsCount) driversPitsNb;
%rename(EndWidth) endWidth;
%rename(EnvMapIndex) envIndex;
%rename(EnvMaps) env; /* TODO: Array */
%rename(EnvMapsCount) envnb;
%rename(Extension) ext;
%rename(Filename) filename;
%rename(FreeCarIndex) freeCarIndex;
%rename(Graphic) graphic;
%rename(HSpace) hSpace;
%rename(Id) id;
%rename(InternalName) internalname;
%rename(KDammage) kDammage;
%rename(KFriction) kFriction;
%rename(KRebound) kRebound;
%rename(KRollRes) kRollRes;
%rename(KRoughWaveLen) kRoughWaveLen;
%rename(KRoughness) kRoughness;
%rename(Length) len;
%rename(Length) length;
%rename(LengthFromStart) lgfromstart;
%rename(Lmax) lmax;
%rename(Lmin) lmin;
%rename(MarksCount) nbMarks;
%rename(Material) material;
%rename(Max) max;
%rename(MaxPitsCount) nMaxPits;
%rename(Min) min;
%rename(Name) name;
%rename(Next) next;
%rename(Normal) normal;
%rename(Params) params_;
%rename(PitCarIndex) pitCarIndex;
%rename(PitEnd) pitEnd;
%rename(PitExit) pitExit;
%rename(PitSegmentCount) nPitSeg;
%rename(PitStart) pitStart;
%rename(Pits) pits;
%rename(Position) pos;
%rename(Previous) prev;
%rename(RaceInfo ) raceInfo ;
%rename(Radius) radius;
%rename(RadiusL) radiusl;
%rename(RadiusR) radiusr;
%rename(RightSideNormal) rgtSideNormal;
%rename(Segment) seg;
%rename(SegmentsCount) nseg;
%rename(Side) side;
%rename(SpeedLimit) speedLimit;
%rename(StartWidth) startWidth;
%rename(Style) style;
%rename(Surface) surface;
%rename(Surfaces) surfaces;
%rename(ToLeft) toLeft;
%rename(ToMiddle) toMiddle;
%rename(ToRight) toRight;
%rename(ToStart) toStart;
%rename(TurnMarksInfo) turnMarksInfo;
%rename(Type) type;
%rename(Type2) type2;
%rename(VSpace) vSpace;
%rename(Version) version;
%rename(Width) width;
%rename(_BackgroundColor) bgColor; /* Exposed as array BackgroundColor */
%rename(_Cars) car;                /* Exposed as array Cars */
%rename(_Marks) marks;             /* Exposed as array Marks */

%cs_array_member(tTrackGraphicInfo, float, BackgroundColor, tFloatArray, _BackgroundColor, 3);
%cs_array_member(tSegExt, int, Marks, tIntArray, _Marks, MarksCount);
%cs_array_member_set_get(tTrackOwnPit, tCarElt, Cars,
                 _SetCarAt, _GetCarAt, TorcsItf.TR_PIT_MAXCARPERPIT);

%include "track.h"

%extend tTrackSeg {
    /* Track RSide and LSide virtual fields. */
    %immutable;
    tTrackSeg *RSide, *LSide;
    tTrackBarrier *BarrierR, *BarrierL;
    %mutable;
    tdble AngleZS, AngleZE, AngleYL, AngleYR, AngleXS, AngleXE, AngleCS;
    t3Dd VertexSL, VertexSR, VertexEL, VertexER;
};

%extend tTrackOwnPit {
    void     _SetCarAt(int index, tCarElt *car) { self->car[index] = car; }
    tCarElt *_GetCarAt(int index)               { return self->car[index]; }
};

%{
/* tTrackSeg */
tdble tTrackSeg_AngleZS_get(tTrackSeg *ts) { return ts->angle[TR_ZS]; }
tdble tTrackSeg_AngleZE_get(tTrackSeg *ts) { return ts->angle[TR_ZE]; }
tdble tTrackSeg_AngleYL_get(tTrackSeg *ts) { return ts->angle[TR_YL]; }
tdble tTrackSeg_AngleYR_get(tTrackSeg *ts) { return ts->angle[TR_YR]; }
tdble tTrackSeg_AngleXS_get(tTrackSeg *ts) { return ts->angle[TR_XS]; }
tdble tTrackSeg_AngleXE_get(tTrackSeg *ts) { return ts->angle[TR_XE]; }
tdble tTrackSeg_AngleCS_get(tTrackSeg *ts) { return ts->angle[TR_CS]; }
void tTrackSeg_AngleZS_set(tTrackSeg *ts, tdble v) { ts->angle[TR_ZS] = v; }
void tTrackSeg_AngleZE_set(tTrackSeg *ts, tdble v) { ts->angle[TR_ZE] = v; }
void tTrackSeg_AngleYL_set(tTrackSeg *ts, tdble v) { ts->angle[TR_YL] = v; }
void tTrackSeg_AngleYR_set(tTrackSeg *ts, tdble v) { ts->angle[TR_YR] = v; }
void tTrackSeg_AngleXS_set(tTrackSeg *ts, tdble v) { ts->angle[TR_XS] = v; }
void tTrackSeg_AngleXE_set(tTrackSeg *ts, tdble v) { ts->angle[TR_XE] = v; }
void tTrackSeg_AngleCS_set(tTrackSeg *ts, tdble v) { ts->angle[TR_CS] = v; }

tTrackBarrier *tTrackSeg_BarrierL_get(tTrackSeg *ts) { return ts->barrier[TR_SIDE_RGT]; }
tTrackBarrier *tTrackSeg_BarrierR_get(tTrackSeg *ts) { return ts->barrier[TR_SIDE_LFT]; }

tTrackSeg *tTrackSeg_RSide_get(tTrackSeg *ts) { return ts->side[TR_SIDE_RGT]; }
tTrackSeg *tTrackSeg_LSide_get(tTrackSeg *ts) { return ts->side[TR_SIDE_LFT]; }

t3Dd* tTrackSeg_VertexSL_get(tTrackSeg *ts) { return &ts->vertex[TR_SL]; }
t3Dd* tTrackSeg_VertexSR_get(tTrackSeg *ts) { return &ts->vertex[TR_SR]; }
t3Dd* tTrackSeg_VertexEL_get(tTrackSeg *ts) { return &ts->vertex[TR_EL]; }
t3Dd* tTrackSeg_VertexER_get(tTrackSeg *ts) { return &ts->vertex[TR_ER]; }
void tTrackSeg_VertexSL_set(tTrackSeg *ts, t3Dd *v) { ts->vertex[TR_SL] = *v; }
void tTrackSeg_VertexSR_set(tTrackSeg *ts, t3Dd *v) { ts->vertex[TR_SR] = *v; }
void tTrackSeg_VertexEL_set(tTrackSeg *ts, t3Dd *v) { ts->vertex[TR_EL] = *v; }
void tTrackSeg_VertexER_set(tTrackSeg *ts, t3Dd *v) { ts->vertex[TR_ER] = *v; }
%}
