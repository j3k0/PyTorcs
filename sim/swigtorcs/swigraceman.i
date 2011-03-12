/* Renaming for tSituation */
%rename(BotSpeed) botSpd;
%rename(CarHandle) carHandle;
%rename(CarInfo) carInfo;
%rename(CarList) carList;
%rename(CarsCount) ncars;
%rename(CurrentCapture) currentCapture;
%rename(CurrentFrame) currentFrame;
%rename(CurrentTime) curTime;
%rename(CurrentTime) currentTime;
%rename(DeltaFrame) deltaFrame;
%rename(DeltaSimu) deltaSimu;
%rename(DeltaTime) deltaTime;
%rename(DisplayMode) displayMode;
%rename(Enabled) enabled;
%rename(Filename) filename;
%rename(FramesPerSecond) fps;
%rename(Fuel) fuel;
%rename(GameScreen) gameScreen;
%rename(GraphicItf) graphicItf;
%rename(Interfaces) itf;
%rename(LapFlag) lapFlag;
%rename(LastFrame) lastFrame;
%rename(LastTime) lastTime;
%rename(MaxDammage) maxDammage;
%rename(MenuScreen) menuScreen;
%rename(ModList) modList;
%rename(MovieCapture) movieCapture;
%rename(Name) name;
%rename(OutputBase) outputBase;
%rename(Params) param;
%rename(Params) params_;
%rename(PlayersCount) nbPlayers;
%rename(PreviousTrackPosition) prevTrkPos;
%rename(RaceEngineInfo) raceEngineInfo;
%rename(RaceInfo) raceInfo;
%rename(RaceMessage) raceMsg;
%rename(RaceName) raceName;
%rename(RefreshDisplay) refreshDisplay;
%rename(RemainingLaps) remainingLaps;
%rename(Results) results;
%rename(RuleState) ruleState;
%rename(Rules) rules;
%rename(Running) running;
%rename(STime) sTime;
%rename(SimItf) simItf;
%rename(Situation) s;
%rename(StartPitTime) startPitTime;
%rename(State) state;
%rename(TimeMult) timeMult;
%rename(TopSpeed) topSpd;
%rename(TotLaps) totLaps;
%rename(TotalPitTime) totalPitTime;
%rename(Track) track;
%rename(TrackItf) trackItf;
%rename(Type) type;
%rename(_Cars) cars; /* Exposed as array Cars */

%cs_array_member_set_get(tSituation, tCarElt, Cars, _SetCarAt, _GetCarAt, RaceInfo.CarsCount);

%include "raceman.h"

%extend tSituation {
    void AddCar(tCarElt *elt);
    tCarElt *_GetCarAt(int index) { return self->cars[index]; }
    void _SetCarAt(int index, tCarElt *value) { self->cars[index] = value; }
};

%{
/* tSituation */
void tSituation_AddCar(tSituation *ts, tCarElt *elt) {
    ts->_ncars += 1;
    if (ts->cars == NULL)
        ts->cars = (tCarElt**)malloc(ts->_ncars * sizeof(tCarElt*));
    else
        ts->cars = (tCarElt**)realloc(ts->cars, ts->_ncars * sizeof(tCarElt*));
    ts->cars[ts->_ncars - 1] = elt;
}
%}
