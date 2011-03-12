%ignore cars; /* Ignore tSituation.cars */
%ignore link; /* TODO: Nested structure of pointers */
%ignore tqh_last; /* TODO: Pointer on pointer on previous last element (really usefull?) */

%rename(AcceleratorCommand) accelCmd;
%rename(BestLapTime) bestLapTime;
%rename(BonnetPosition) bonnetPos;
%rename(BrakeCommand) brakeCmd;
%rename(BrakeDiskRadius) brakeDiskRadius;
%rename(BrakeTemperature) brakeTemp;
%rename(CarHandle) carHandle;
%rename(CarName) carName;
%rename(Category) category;
%rename(ClutchCommand) clutchCmd;
%rename(Collision) collision;
%rename(CollisionCount) collision_count;
%rename(CollisionPosition) collpos;
%rename(CollisionState) collision_state;
%rename(Condition) condition;
%rename(Ctrl) ctrl;
%rename(Ctrl) ctrl;
%rename(CurLapTime) curLapTime;
%rename(CurTime) curTime;
%rename(Dammage) dammage;
%rename(Debug) debug;
%rename(DeltaBestLapTime) deltaBestLapTime;
%rename(Dimension) dimension;
%rename(DistFromStartLine) distFromStartLine;
%rename(DistRaced) distRaced;
%rename(DriverIndex) driverIndex;
%rename(DriverPosition) drvPos;
%rename(DriverType) driverType;
%rename(EngineMaxPw) engineMaxPw;
%rename(EngineMaxTq) engineMaxTq;
%rename(EngineRpm) enginerpm;
%rename(EngineRpmMax) enginerpmMax;
%rename(EngineRpmMaxPw) enginerpmMaxPw;
%rename(EngineRpmMaxTq) enginerpmMaxTq;
%rename(EngineRpmRedLine) enginerpmRedLine;
%rename(Event) event_;
%rename(ExhaustPositionsCount) exhaustNb;
%rename(ExhaustPower) exhaustPower;
%rename(First) tqh_first;
%rename(Force) force;
%rename(Fuel) fuel;
%rename(Fuel) fuel;
%rename(FuelConsumptionInstant) fuel_consumption_instant;
%rename(FuelConsumptionTotal) fuel_consumption_total;
%rename(Gear) gear;
%rename(GearNb) gearNb;
%rename(GearOffset) gearOffset;
%rename(Index) index;
%rename(Info) info;
%rename(LapToClear) lapToClear;
%rename(Laps) laps;
%rename(LapsBehindLeader) lapsBehindLeader;
%rename(LastLapTime) lastLapTime;
%rename(LightCommand) lightCmd;
%rename(Messages) msg; /* TODO: Array of 4 strings */
%rename(ModName) modName;
%rename(Name) name;
%rename(NbPitStops) nbPitStops;
%rename(Next) next;
%rename(Normal) normal;
%rename(ParamsHandle) paramsHandle;
%rename(Penalty) penalty;
%rename(PenaltyList) penaltyList;
%rename(Pit) pit;
%rename(PitCommand) pitcmd;
%rename(Position) pos;
%rename(PositionMatrix) posMat;
%rename(Priv) priv;
%rename(Pub) pub;
%rename(Race) race;
%rename(RaceCommand) raceCmd;
%rename(RaceNumber) raceNumber;
%rename(RelativePosition) relPos;
%rename(RemainingLaps) remainingLaps;
%rename(Repair) repair;
%rename(RimRadius) rimRadius;
%rename(RobotItf) robot;
%rename(RollingResistance) rollRes;
%rename(ScheduledEventTime) scheduledEventTime;
%rename(Segment) seg;
%rename(SkillLevel) skillLevel;
%rename(SkillLevel) skillLevel;
%rename(SlipAccel) slipAccel;
%rename(SlipSide) slipSide;
%rename(Smoke) smoke;
%rename(SpinVelocity) spinVel;
%rename(StartRank) startRank;
%rename(StatGC) statGC;
%rename(State) state;
%rename(SteerCommand) steer;
%rename(SteerLock) steerLock;
%rename(StopType) stopType;
%rename(Tank) tank;
%rename(TeamName) teamname;
%rename(TemperatureIn) temp_in;
%rename(TemperatureMid) temp_mid;
%rename(TemperatureOut) temp_out;
%rename(TimeBeforeNext) timeBeforeNext;
%rename(TimeBehindLeader) timeBehindLeader;
%rename(TimeBehindPrev) timeBehindPrev;
%rename(TireHeight) tireHeight;
%rename(TireWidth) tireWidth;
%rename(ToLeft) toLeft;
%rename(ToMiddle) toMiddle;
%rename(ToRight) toRight;
%rename(ToStart) toStart;
%rename(TopSpeed) topSpeed;
%rename(TrackPosition) trkPos;
%rename(VisualAttr) visualAttr;
%rename(WheelRadius) wheelRadius;
%rename(_Corners) corner;              /* Exposed as array Corners */
%rename(_ExhaustPositions) exhaustPos; /* Exposed as array ExhaustPositions */
%rename(_GearsRatio) gearRatio;        /* Exposed as array GearsRatio */
%rename(_IconColor) iconColor;         /* Exposed as array IconColor */
%rename(_MessageColor) msgColor;       /* Exposed as array MessageColor */
%rename(_Reactions) reaction;          /* Exposed as array Reactions */
%rename(_Skids) skid;                  /* Exposed as array Skids */
%rename(_Wheels) wheel;                /* Exposed as array Wheels */

%cs_array_member(tCarCtrl, float, MessageColor, tFloatArray, _MessageColor, 4);
%cs_array_member(tInitCar, float, IconColor, tFloatArray, _IconColor, 3);
%cs_array_member(tInitCar, tWheelSpec, Wheels, tWheelSpecArray, _Wheels, 4);
%cs_array_member(tPrivCar, float, GearsRatio, tFloatArray, _GearsRatio, MAX_GEARS);
%cs_array_member(tPrivCar, float, Reactions, tFloatArray, _Reactions, 4);
%cs_array_member(tPrivCar, float, Skids, tFloatArray, _Skids, 4);
%cs_array_member(tPrivCar, tPosd, Corners, tPosdArray, _Corners, 4);
%cs_array_member(tPrivCar, tWheelState, Wheels, tWheelStateArray, _Wheels, 4);
%cs_array_member(tPublicCar, tPosd, Corners, tPosdArray, _Corners, 4);
%cs_array_member(tVisualAttributes, t3Dd, ExhaustPositions, t3DdArray, _ExhaustPositions, ExhaustPositionsCount);

%typemap(cscode) tCarElt %{
  public String ModName {
    get { return Priv.ModName; }
    set { Priv.ModName = value; }
  }
  public tDynPt DynGC { get { return Pub.DynGC; } }
  public tPosd Position { get { return Pub.DynGC.Position; } }
  public tPosd Speed { get { return Pub.DynGC.Velocity; } }
  public tPosd Acceleration { get { return Pub.DynGC.Acceleration; } }
  public int State { get { return Pub.State; } }
  public String Name { get { return Info.Name; } }
  public String FileName { get { 
    string team = Info.TeamName;
    return "cars" + System.IO.Path.DirectorySeparatorChar + team
      + System.IO.Path.DirectorySeparatorChar + team + ".xml";
  }}
  public Math3D.Matrix4 PositionMatrix { get { return Pub.PositionMatrix; } }
%}

%include "car.h"

