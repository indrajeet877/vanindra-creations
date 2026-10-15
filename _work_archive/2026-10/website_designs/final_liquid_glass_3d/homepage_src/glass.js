/* VanIndra glass orbit: a tiny WebGL1 renderer, no libraries.
   A rounded-rect glass ribbon swept round a circle (one twist), posed as an orbit round the hero phone.
   Pass 1 writes back-face normals + depth to a texture; pass 2 draws the front faces as clear glass:
   refraction in and out per colour channel (soft dispersion), light emerald absorption, a thin Fresnel rim
   and a pointer-driven specular light. The body is only partly opaque, so the real page shows through.
   Occlusion: the half of the orbit that lies behind the phone plane is cut out where the phone is
   (uOcc 0), or drawn alone (uOcc 1, the "back" still) / the front half alone (uOcc 2, the "front" still). */
function createGlassHalo(canvas, opts) {
  opts = opts || {};
  var gl = opts.gl || canvas.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: opts.aa !== false, depth: true, stencil: false, powerPreference: 'default', preserveDrawingBuffer: !!opts.keep });
  if (!gl) return null;
  var NU = opts.nu || 192, NV = opts.nv || 24, HW = 0.2, HH = 0.068, RAD = 0.058;
  var per = [];
  (function () {
    var ax = HW - RAD, ay = HH - RAD, q = Math.PI * RAD / 2, L = 4 * ax + 4 * ay + 4 * q;
    var seg = [2 * ay, q, 2 * ax, q, 2 * ay, q, 2 * ax, q];
    for (var i = 0; i < NV; i++) {
      var s = (i / NV) * L, k = 0, x, y, nx, ny;
      while (k < 7 && s > seg[k]) { s -= seg[k]; k++; }
      if (k === 0) { x = HW; y = -ay + s; nx = 1; ny = 0; }
      else if (k === 2) { x = ax - s; y = HH; nx = 0; ny = 1; }
      else if (k === 4) { x = -HW; y = ay - s; nx = -1; ny = 0; }
      else if (k === 6) { x = -ax + s; y = -HH; nx = 0; ny = -1; }
      else { var ci = (k - 1) / 2, a0 = ci * Math.PI / 2 + s / RAD; nx = Math.cos(a0); ny = Math.sin(a0); x = (ci === 0 || ci === 3 ? ax : -ax) + RAD * nx; y = (ci < 2 ? ay : -ay) + RAD * ny; }
      per.push([x, y, nx, ny]);
    }
  })();
  var nVert = NU * NV, qd = new Float32Array(nVert * 4), uu = new Float32Array(nVert * 2), i, j;
  for (i = 0; i < NU; i++) for (j = 0; j < NV; j++) {
    var o = i * NV + j, p = per[j];
    qd[o * 4] = p[0]; qd[o * 4 + 1] = p[1]; qd[o * 4 + 2] = p[2]; qd[o * 4 + 3] = p[3];
    uu[o * 2] = i / NU; uu[o * 2 + 1] = j / NV;
  }
  var idx = new Uint16Array(NU * NV * 6), w = 0;
  for (i = 0; i < NU; i++) for (j = 0; j < NV; j++) {
    var i2 = (i + 1) % NU, A = i * NV + j, B = i * NV + (j + 1) % NV, C = i2 * NV + j, D = i2 * NV + (j + 1) % NV;
    idx[w++] = A; idx[w++] = C; idx[w++] = B; idx[w++] = B; idx[w++] = C; idx[w++] = D;
  }
  // the twist is done in the vertex shader (uPhase rolls the ribbon); uFoc is the focal length in half-heights
  var VS = 'precision highp float;attribute vec4 aQ;attribute vec2 aU;uniform mat3 uM;uniform vec3 uOff;uniform float uCam,uAsp,uFoc,uSh,uPhase;varying vec3 vW,vN;varying float vQ;'
    + 'void main(){float u=aU.x*6.2831853,cu=cos(u),su=sin(u),t=u+uPhase,ct=cos(t),st=sin(t);'
    + 'float a=aQ.x*ct-aQ.y*st,b=aQ.x*st+aQ.y*ct,na=aQ.z*ct-aQ.w*st,nb=aQ.z*st+aQ.w*ct;'
    + 'vec3 P=vec3((1.+a)*cu,(1.+a)*su,b),N=vec3(na*cu,na*su,nb);'
    + 'vQ=abs(fract(aU.x-.25)-.5)*2.;'
    + 'vec3 w=uM*P+uOff;vW=w;vN=uM*N;vec3 v=w-vec3(0.,0.,uCam);float z=-v.z;gl_Position=vec4(v.x*uFoc/uAsp,v.y*uFoc+uSh*z,((z-.5)/9.5*2.-1.)*z,z);}';
  var FB = 'precision highp float;uniform float uCam;varying vec3 vW,vN;void main(){vec3 n=normalize(vN);float d=length(vW-vec3(0.,0.,uCam));gl_FragColor=vec4(n*.5+.5,clamp((d-uCam+2.)/4.,0.,1.));}';
  var FF = 'precision highp float;uniform sampler2D uBack;uniform vec2 uRes,uLight;uniform vec3 uOff;uniform vec4 uPh;uniform float uCam,uWarm,uDisp,uSweep,uDark,uOcc,uPhR;varying vec3 vW,vN;varying float vQ;'
    // the studio the glass sees: ivory walls, an emerald floor, two soft gold lights (or a dark emerald studio)
    + 'vec3 env(vec3 d){vec3 g=mix(vec3(1.,.96,.88),vec3(1.5,1.08,.42),uWarm);float ax=abs(d.x),y=d.y;vec3 c;'
    + 'if(uDark<.5){c=vec3(1.,.988,.958)*(.9+.12*smoothstep(-.2,.9,y));c=mix(c,vec3(.04,.21,.15),smoothstep(-.02,-.55,y)*.92);'
    + 'c=mix(c,vec3(.10,.36,.27),smoothstep(.05,0.,abs(ax-.45)-.08)*.35*smoothstep(-.6,.2,y));c+=g*(exp(-(ax-.62)*(ax-.62)*90.)*smoothstep(-.5,.5,y)*.9+exp(-ax*ax*220.)*smoothstep(.1,.8,y)*.6);}'
    + 'else{c=vec3(.03,.09,.07)+vec3(.05,.17,.12)*smoothstep(-.5,.6,y)+vec3(.05,.42,.28)*exp(-(ax-.42)*(ax-.42)*25.)*smoothstep(-.8,.3,y)*.5'
    + '+g*(exp(-(ax-.66)*(ax-.66)*81.)*smoothstep(-.4,.5,y)*.95+exp(-ax*ax*144.)*smoothstep(.1,.8,y)*.45);}return c;}'
    + 'float phoneSD(vec2 p){vec2 c=(uPh.xy+uPh.zw)*.5,h=(uPh.zw-uPh.xy)*.5;vec2 q=abs(p-c)-h+uPhR;return length(max(q,0.))+min(max(q.x,q.y),0.)-uPhR;}'
    + 'void main(){float zr=vW.z-uOff.z;if(uOcc>.5&&uOcc<1.5&&zr>=0.)discard;if(uOcc>1.5&&zr<0.)discard;'
    + 'float sd=phoneSD(gl_FragCoord.xy),occ=1.;if(uOcc<.5&&zr<0.){occ=clamp(sd+.5,0.,1.);if(occ<=0.)discard;}'
    + 'float over=uOcc<.5?1.-clamp(sd+.5,0.,1.):0.;'
    + 'vec3 cam=vec3(0.,0.,uCam),rd=normalize(vW-cam),n=normalize(vN);if(dot(n,rd)>0.)n=-n;'
    + 'vec4 bk=texture2D(uBack,gl_FragCoord.xy/uRes);vec3 nb=bk.a>0.?normalize(bk.xyz*2.-1.):n;float th=bk.a>0.?max(bk.a*4.+uCam-2.-length(vW-cam),.02):.12;'
    + 'float ndv=clamp(dot(-rd,n),0.,1.),F=.03+.97*pow(1.-ndv,5.);vec3 r1=refract(rd,n,.7519);float dv=.012*uDisp*smoothstep(.02,.4,ndv);'
    + 'vec3 a=refract(r1,-nb,1.33-dv),b=refract(r1,-nb,1.33),e=refract(r1,-nb,1.33+dv);if(min(dot(a,a),min(dot(b,b),dot(e,e)))<.01){a=reflect(r1,-nb);b=a;e=a;}'
    + 'vec3 tr=vec3(env(a).r,env(b).g,env(e).b)*exp(-th*mix(vec3(.38,.07,.21),vec3(.22,.05,.12),uDark));'
    + 'float l=dot(tr,vec3(.299,.587,.114));tr=mix(vec3(l)*vec3(.94,.97,1.02),tr,mix(.4,1.,uWarm));'
    // clear body: partly opaque, thinner over the phone screen so the real screen shows through
    + 'float tk=smoothstep(.04,.34,th),body=mix(mix(.36,.6,tk),mix(.12,.24,tk),over);if(uDark>.5)body=mix(mix(.42,.62,tk),mix(.10,.22,tk),over);'
    + 'vec3 rf=env(reflect(rd,n));float rim=pow(1.-ndv,7.);'
    + 'vec3 L=normalize(vec3(uLight,1.2));float sp=pow(max(dot(reflect(rd,n),L),0.),110.);'
    + 'float sw=uSweep<0.?0.:exp(-(vQ-uSweep)*(vQ-uSweep)*81.);'
    + 'vec3 rimc=mix(vec3(1.,1.,.98),vec3(1.,.86,.52),.55*uWarm);'
    + 'float al=clamp(body*(1.-F)+F*.85,0.,1.);'
    + 'vec3 col=tr*body*(1.-F)+rf*F*.85;if(uDark<.5){float eg=smoothstep(.42,.06,ndv)*(1.-over);col=mix(col,vec3(.03,.17,.12)*al,eg*.42);}col=col/(1.+col*.12);'
    + 'sp*=1.-over*.6;col+=rimc*rim*.55+vec3(1.,.96,.88)*sp*1.3+vec3(1.,.84,.5)*sw*.5;al=clamp(al+rim*.45+sp*.6+sw*.25,0.,1.);'
    + 'gl_FragColor=vec4(col,al)*occ;}';
  function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
  function prog(fs) { var p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.bindAttribLocation(p, 0, 'aQ'); gl.bindAttribLocation(p, 1, 'aU'); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); return p; }
  var pB = prog(FB), pF = prog(FF);
  function buf(data, tgt) { var b = gl.createBuffer(); gl.bindBuffer(tgt, b); gl.bufferData(tgt, data, gl.STATIC_DRAW); return b; }
  [[qd, 4], [uu, 2]].forEach(function (d, k) { buf(d[0], gl.ARRAY_BUFFER); gl.enableVertexAttribArray(k); gl.vertexAttribPointer(k, d[1], gl.FLOAT, false, 0, 0); });
  buf(idx, gl.ELEMENT_ARRAY_BUFFER);
  var NAMES = ['uM', 'uOff', 'uCam', 'uAsp', 'uFoc', 'uSh', 'uPhase', 'uBack', 'uRes', 'uWarm', 'uDisp', 'uLight', 'uSweep', 'uDark', 'uOcc', 'uPh', 'uPhR'];
  function locs(p) { var o = {}; NAMES.forEach(function (n) { o[n] = gl.getUniformLocation(p, n); }); return o; }
  var LB = locs(pB), LF = locs(pF), tex = null, fbo = null, rbo = null, W = 0, H = 0;
  function resize(w, h) {
    w = Math.max(2, Math.round(w)); h = Math.max(2, Math.round(h)); if (w === W && h === H) return false;
    W = w; H = h; canvas.width = w; canvas.height = h;
    if (tex) { gl.deleteTexture(tex); gl.deleteFramebuffer(fbo); gl.deleteRenderbuffer(rbo); }
    tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    [gl.TEXTURE_MIN_FILTER, gl.TEXTURE_MAG_FILTER].forEach(function (k) { gl.texParameteri(gl.TEXTURE_2D, k, gl.NEAREST); });
    [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T].forEach(function (k) { gl.texParameteri(gl.TEXTURE_2D, k, gl.CLAMP_TO_EDGE); });
    rbo = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, rbo); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, w, h);
    fbo = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
    gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, rbo);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return true;
  }
  function mul(a, b) { var o = [], i, j, k, t; for (i = 0; i < 3; i++) for (j = 0; j < 3; j++) { t = 0; for (k = 0; k < 3; k++) t += a[k * 3 + j] * b[i * 3 + k]; o[i * 3 + j] = t; } return o; }
  function mat(yaw, pitch, roll) {
    var c = Math.cos, s = Math.sin;
    var m = mul([c(roll), s(roll), 0, -s(roll), c(roll), 0, 0, 0, 1], mul([1, 0, 0, 0, c(pitch), s(pitch), 0, -s(pitch), c(pitch)], [c(yaw), 0, -s(yaw), 0, 1, 0, s(yaw), 0, c(yaw)]));
    return new Float32Array([m[0], m[3], m[6], m[1], m[4], m[7], m[2], m[5], m[8]]);
  }
  // S.ph = the phone's rounded rect in canvas pixels (x0, y0, x1, y1 from the bottom-left, as gl_FragCoord), S.phr its corner radius
  var S = { yaw: 0, pitch: 1.0, roll: 0, phase: 0, ox: 0, oy: 0, oz: 0, cam: 3.9, foc: 2.5, sh: 0, warm: 1, disp: 1, lx: -0.4, ly: 0.6, sweep: -1, dark: 0, occ: 0, ph: [-9, -9, -8, -8], phr: 1 };
  function common(L, M) {
    gl.uniformMatrix3fv(L.uM, false, M); gl.uniform3f(L.uOff, S.ox, S.oy, S.oz); gl.uniform1f(L.uCam, S.cam); gl.uniform1f(L.uAsp, W / H);
    gl.uniform1f(L.uFoc, S.foc); gl.uniform1f(L.uSh, S.sh); gl.uniform1f(L.uPhase, S.phase);
  }
  function render() {
    var M = mat(S.yaw, S.pitch, S.roll);
    gl.enable(gl.DEPTH_TEST); gl.enable(gl.CULL_FACE); gl.clearColor(0, 0, 0, 0); gl.clearDepth(1);
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo); gl.viewport(0, 0, W, H); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(pB); gl.cullFace(gl.FRONT); common(LB, M);
    gl.drawElements(gl.TRIANGLES, idx.length, gl.UNSIGNED_SHORT, 0);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(pF); gl.cullFace(gl.BACK); common(LF, M);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(LF.uBack, 0);
    gl.uniform2f(LF.uRes, W, H); gl.uniform1f(LF.uWarm, S.warm); gl.uniform1f(LF.uDisp, S.disp); gl.uniform2f(LF.uLight, S.lx, S.ly);
    gl.uniform1f(LF.uSweep, S.sweep); gl.uniform1f(LF.uDark, S.dark); gl.uniform1f(LF.uOcc, S.occ);
    gl.uniform4f(LF.uPh, S.ph[0], S.ph[1], S.ph[2], S.ph[3]); gl.uniform1f(LF.uPhR, S.phr);
    gl.drawElements(gl.TRIANGLES, idx.length, gl.UNSIGNED_SHORT, 0);
  }
  return { gl: gl, S: S, resize: resize, render: render, size: function () { return [W, H]; } };
}
/* Fit the orbit into a canvas: samples the outer silhouette over the whole pose range
   (pitch p0-0.2 .. p0+0.32, yaw +-0.36) and returns the focal length, vertical shift and aspect,
   plus k = canvas width per CSS px of the default lobe radius. */
function fitGlassPose(p0, cam) {
  cam = cam || 3.9;
  var c = Math.cos, s = Math.sin, xh = 0, y0 = 1e9, y1 = -1e9;
  for (var pi = 0; pi <= 6; pi++) for (var yi = -2; yi <= 2; yi++) {
    var P = p0 - 0.2 + pi * 0.52 / 6, Y = yi * 0.18;
    for (var ui = 0; ui < 72; ui++) {
      var u = ui / 72 * 6.2832;
      for (var r = 0.78; r < 1.3; r += 0.44) for (var b = -0.22; b < 0.3; b += 0.44) {
        var x = r * c(u), y = r * s(u), z = b;
        var x1 = x * c(Y) + z * s(Y), z1 = -x * s(Y) + z * c(Y);
        var y2 = y * c(P) - z1 * s(P), z2 = y * s(P) + z1 * c(P);
        // same handedness as mat(): positive pitch sends the top of the ring away from the camera
        var d = cam + z2, px = x1 / d, py = y2 / d;
        if (Math.abs(px) > xh) xh = Math.abs(px); if (py < y0) y0 = py; if (py > y1) y1 = py;
      }
    }
  }
  var foc = 1.88 / (y1 - y0), sh = -foc * (y1 + y0) / 2, asp = foc * xh / 0.94;
  var lobe = 1.2 / cam * foc / asp; // ndc x of the default lobe
  return { foc: foc, sh: sh, asp: asp, lobe: lobe };
}
