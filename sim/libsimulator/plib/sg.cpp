#include "sg.h"
#include <math.h>

void sgMakeCoordMat4 ( sgMat4 m, const SGfloat x, const SGfloat y, const SGfloat z, const SGfloat h, const SGfloat p, const SGfloat r )
{
  SGfloat ch, sh, cp, sp, cr, sr, srsp, crsp, srcp ;

  if ( h == SG_ZERO )
  {
    ch = SG_ONE ;
    sh = SG_ZERO ;
  }
  else
  {
    sh = (SGfloat) sin( h * SG_DEGREES_TO_RADIANS ) ;
    ch = (SGfloat) cos( h * SG_DEGREES_TO_RADIANS ) ;
  }

  if ( p == SG_ZERO )
  {
    cp = SG_ONE ;
    sp = SG_ZERO ;
  }
  else
  {
    sp = (SGfloat) sin( p * SG_DEGREES_TO_RADIANS ) ;
    cp = (SGfloat) cos( p * SG_DEGREES_TO_RADIANS ) ;
  }

  if ( r == SG_ZERO )
  {
    cr   = SG_ONE ;
    sr   = SG_ZERO ;
    srsp = SG_ZERO ;
    srcp = SG_ZERO ;
    crsp = sp ;
  }
  else
  {
    sr   = (SGfloat) sin( r * SG_DEGREES_TO_RADIANS ) ;
    cr   = (SGfloat) cos( r * SG_DEGREES_TO_RADIANS ) ;
    srsp = sr * sp ;
    crsp = cr * sp ;
    srcp = sr * cp ;
  }

  m[0][0] = (SGfloat)(  ch * cr - sh * srsp ) ;
  m[1][0] = (SGfloat)( -sh * cp ) ;
  m[2][0] = (SGfloat)(  sr * ch + sh * crsp ) ;
  m[3][0] =  x ;

  m[0][1] = (SGfloat)( cr * sh + srsp * ch ) ;
  m[1][1] = (SGfloat)( ch * cp ) ;
  m[2][1] = (SGfloat)( sr * sh - crsp * ch ) ;
  m[3][1] =  y ;

  m[0][2] = (SGfloat)( -srcp ) ;
  m[1][2] = (SGfloat)(  sp ) ;
  m[2][2] = (SGfloat)(  cr * cp ) ;
  m[3][2] =  z ;

  m[0][3] =  SG_ZERO ;
  m[1][3] =  SG_ZERO ;
  m[2][3] =  SG_ZERO ;
  m[3][3] =  SG_ONE ;
}
