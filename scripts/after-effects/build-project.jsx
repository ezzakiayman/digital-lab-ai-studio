#target aftereffects
// Digital Lab. Build the editable project next to this script in an extracted package.
(function () {
    var base = File($.fileName).parent;
    var fps, project, footageFolder, sceneFolder, master, white;
    var imported = {}, context = '', undoStarted = false;
    var has = Object.prototype.hasOwnProperty;
    function owned(object, key) { return has.call(object, key); }

    // ExtendScript versions which do not provide JSON.parse also accept this data-only reader.
    function parseData(s) {
        s = s.replace(/^\uFEFF/, '');
        if (typeof JSON !== 'undefined' && typeof JSON.parse === 'function') return JSON.parse(s);
        var i = 0;
        function bad() { throw Error('JSON incorrect au caractère ' + i); }
        function skip() { while (i < s.length && /\s/.test(s.charAt(i))) i++; }
        function string() {
            var result = '', c, h;
            if (s.charAt(i++) !== '"') bad();
            while (i < s.length) {
                c = s.charAt(i++);
                if (c === '"') return result;
                if (c === '\\') {
                    c = s.charAt(i++);
                    if (c === 'u') {
                        h = s.substr(i, 4);
                        if (!/^[0-9a-f]{4}$/i.test(h)) bad();
                        result += String.fromCharCode(parseInt(h, 16)); i += 4;
                    } else if (c === '"' || c === '/' || c === '\\') result += c;
                    else {
                        var escaped = {b:'\b', f:'\f', n:'\n', r:'\r', t:'\t'};
                        if (!owned(escaped, c)) bad();
                        result += escaped[c];
                    }
                } else { if (c.charCodeAt(0) < 32) bad(); result += c; }
            }
            bad();
        }
        function value() {
            skip();
            var c = s.charAt(i), result, k, token;
            if (c === '"') return string();
            if (c === '{' || c === '[') {
                var obj = c === '{', end = obj ? '}' : ']';
                i++; result = obj ? {} : []; skip();
                if (s.charAt(i) === end) { i++; return result; }
                while (i < s.length) {
                    if (obj) {
                        skip(); k = string(); skip();
                        if (k === '__proto__' || s.charAt(i++) !== ':') bad();
                        result[k] = value();
                    } else result.push(value());
                    skip(); c = s.charAt(i++);
                    if (c === end) return result;
                    if (c !== ',') bad();
                }
                bad();
            }
            if (s.substr(i, 4) === 'true') { i += 4; return true; }
            if (s.substr(i, 5) === 'false') { i += 5; return false; }
            if (s.substr(i, 4) === 'null') { i += 4; return null; }
            token = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/.exec(s.slice(i, i+64));
            if (!token) bad();
            i += token[0].length;
            return Number(token[0]);
        }
        var result = value(); skip(); if (i !== s.length) bad(); return result;
    }
    function localFile(relative) {
        if (typeof relative !== 'string' || !relative || /(^[\/\\]|:|(?:^|[\/\\])\.\.(?:[\/\\]|$))/.test(relative))
            throw Error('Chemin relatif invalide dans le projet.');
        return new File(base.fsName + '/' + relative);
    }
    function loadData() {
        var file = localFile('project.json');
        file.encoding = 'UTF-8';
        if (!file.open('r')) throw Error('project.json est introuvable. Extraire le ZIP en entier avant de lancer le script.');
        var raw;
        try { raw = file.read(); } finally { file.close(); }
        return parseData(raw);
    }
    function track(a) { return a !== null && a !== undefined && typeof a === 'object' && a.keys instanceof Array; }
    function first(a) { return track(a) ? a.keys[0][1] : a; }
    function animated(a) { return track(a) && a.keys.length > 1; }
    function identity(v) { return v; }
    function shape(s) {
        var sh = new Shape(), flat = [], i;
        for (i = 0; i < s.vertices.length; i++) flat.push([0,0]);
        sh.vertices = s.vertices;
        sh.inTangents = s.inTangents || flat;
        sh.outTangents = s.outTangents || flat;
        sh.closed = !!s.closed;
        return sh;
    }
    function set(p, data, convert) {
        if (data === undefined || data === null) return;
        convert = convert || identity;
        if (!animated(data)) { p.setValue(convert(first(data))); return; }
        var times = [], values = [], i;
        for (i = 0; i < data.keys.length; i++) {
            times.push(data.keys[i][0]/fps); values.push(convert(data.keys[i][1]));
        }
        p.setValuesAtTimes(times, values);
        var linear = KeyframeInterpolationType.LINEAR, hold = KeyframeInterpolationType.HOLD;
        var supportsLinear = p.isInterpolationTypeValid(linear);
        for (i = 1; i <= times.length; i++) {
            var left = i > 1 && data.keys[i-2][2] === 'hold' ? hold : linear;
            var right = data.keys[i-1][2] === 'hold' ? hold : linear;
            // Bezier positions must have straight spatial segments between sampled positions.
            if (p.isSpatial) {
                var z = p.value.length === 3 ? [0,0,0] : [0,0];
                p.setSpatialAutoBezierAtKey(i,false);
                p.setSpatialContinuousAtKey(i,false);
                p.setSpatialTangentsAtKey(i,z,z);
            }
            p.setInterpolationTypeAtKey(i,supportsLinear ? left : hold,supportsLinear ? right : hold);
        }
    }
    function rgba(c) { return [c[0], c[1], c[2], c.length > 3 ? c[3] : 1]; }
    function rgb(c) { return [c[0], c[1], c[2]]; }
    function footage(relative) {
        var key = '$' + relative;
        if (!owned(imported,key)) {
            var file = localFile(relative);
            if (!file.exists) throw Error('Média manquant : '+relative);
            var item = project.importFile(new ImportOptions(file));
            item.parentFolder = footageFolder; imported[key] = item;
        }
        return imported[key];
    }
    function background(comp) {
        var layer;
        if (!white) {
            layer = comp.layers.addSolid([1,1,1],'Papier blanc',comp.width,comp.height,1,comp.duration);
            white = layer.source; white.parentFolder = footageFolder;
        } else layer = comp.layers.add(white,comp.duration);
        layer.name = 'Fond blanc'; layer.startTime=0; layer.inPoint=0;
        layer.outPoint=comp.duration; layer.locked=true;
    }
    function readAt(a, frame) {
        if (!track(a)) return a;
        var k = a.keys, low = 0, high = k.length-1, m;
        while (low < high) { m = Math.ceil((low+high)/2); if(k[m][0]<=frame) low=m; else high=m-1; }
        if (low === k.length-1 || frame <= k[low][0] || k[low][2] === 'hold') return k[low][1];
        var f = (frame-k[low][0])/(k[low+1][0]-k[low][0]);
        var v = k[low][1], next = k[low+1][1], j, out = [];
        if (v instanceof Array) {
            for (j=0;j<v.length;j++) out[j]=v[j]+(next[j]-v[j])*f;
            return out;
        }
        if (typeof v === 'number') return v+(next-v)*f;
        return v;
    }
    function textLayer(comp,d) {
        var layer = comp.layers.addText(' ');
        var p=layer.property('ADBE Text Properties').property('ADBE Text Document');
        var times={}, frames=[], i, j, v;
        var input=[d.text,d.font,d.size], key;
        for(i=0;i<input.length;i++) if (animated(input[i])) {
            for(j=0;j<input[i].keys.length;j++) times[input[i].keys[j][0]]=true;
        }
        var sourceAnimated=false;
        for(key in times) if (owned(times,key)) {frames.push(Number(key));sourceAnimated=true;}
        frames.push(d.start || 0);frames.sort(function(a,b){return a-b;});
        var previous=-1;
        for(i=0;i<frames.length;i++) {
            var frame=frames[i];if(frame===previous) continue;previous=frame;
            v=new TextDocument(String(readAt(d.text,frame)));
            v.resetCharStyle(); v.resetParagraphStyle();
            v.font=readAt(d.font,frame) || 'ArialMT'; v.fontSize=readAt(d.size,frame) || 64;
            v.justification=d.justify==='center'?ParagraphJustification.CENTER_JUSTIFY:d.justify==='right'?ParagraphJustification.RIGHT_JUSTIFY:ParagraphJustification.LEFT_JUSTIFY;
            v.applyFill=true;v.applyStroke=false;v.fillColor=rgb(first(d.fill) || [0,0,0]);
            if (sourceAnimated) p.setValueAtTime(frame/fps,v); else p.setValue(v);
        }
        // Animate changing ink independently of Source Text so the editor types the wording just once.
        if (animated(d.fill)) {
            var animator=layer.property('ADBE Text Properties').property('ADBE Text Animators').addProperty('ADBE Text Animator');
            animator.name='Couleur du texte';
            animator.property('ADBE Text Selectors').addProperty('ADBE Text Selector');
            set(animator.property('ADBE Text Animator Properties').addProperty('ADBE Text Fill Color'),d.fill,rgba);
        }
        return layer;
    }
    function drawShape(layer,d) {
        var contents=layer.property('ADBE Root Vectors Group');
        var group=contents.addProperty('ADBE Vector Group');
        group.name=d.name;
        var items=group.property('ADBE Vectors Group');
        var paths=d.paths || [{path:d.path}], i;
        for (i=0;i<paths.length;i++) {
            var pathGroup=items.addProperty('ADBE Vector Shape - Group');
            pathGroup.name=paths[i].name || 'Tracé';
            set(pathGroup.property('ADBE Vector Shape'),paths[i].path,shape);
        }
        if (d.fill!==undefined && d.fill!==null && first(d.fill)!==null) {
            var fill=items.addProperty('ADBE Vector Graphic - Fill');
            set(fill.property('ADBE Vector Fill Color'),d.fill,rgba);
            set(fill.property('ADBE Vector Fill Opacity'),d.fillOpacity);
        }
        if (d.stroke!==undefined && d.stroke!==null && first(d.stroke)!==null) {
            var stroke=items.addProperty('ADBE Vector Graphic - Stroke');
            set(stroke.property('ADBE Vector Stroke Color'),d.stroke,rgba);
            set(stroke.property('ADBE Vector Stroke Width'),d.strokeWidth===undefined?1:d.strokeWidth);
            set(stroke.property('ADBE Vector Stroke Opacity'),d.strokeOpacity);
            if(d.lineCap) stroke.property('ADBE Vector Stroke Line Cap').setValue({butt:1,round:2,square:3}[d.lineCap]);
            if(d.lineJoin) stroke.property('ADBE Vector Stroke Line Join').setValue({miter:1,round:2,bevel:3}[d.lineJoin]);
        }
        if (d.trimEnd!==undefined && (animated(d.trimEnd) || first(d.trimEnd)!==100)) {
            var trim=items.addProperty('ADBE Vector Filter - Trim');
            set(trim.property('ADBE Vector Trim End'),d.trimEnd);
        }
    }
    function clipRect(layer,d) {
        if (!d.maskRect) return;
        var prop=layer.property('ADBE Mask Parade').addProperty('ADBE Mask Atom');
        prop.name='Révélation';prop.maskMode=MaskMode.ADD;
        var path=prop.property('ADBE Mask Shape'), keys=[], last=null, points, rect, pos, scale, r, f, i;
        function samePoints(a,b) {
            if (!a || !b) return false;
            for(var j=0;j<4;j++) if(Math.abs(a[j][0]-b[j][0])>0.0001||Math.abs(a[j][1]-b[j][1])>0.0001)return false;
            return true;
        }
        for(f=d.start;f<d.end;f++) {
            rect=readAt(d.maskRect,f);pos=readAt(d.position,f)||[0,0];scale=readAt(d.scale,f)||[100,100];
            r=(readAt(d.rotation,f)||0)*Math.PI/180;
            points=[[rect[0],rect[1]],[rect[0]+rect[2],rect[1]],[rect[0]+rect[2],rect[1]+rect[3]],[rect[0],rect[1]+rect[3]]];
            for(i=0;i<4;i++) {
                var x=points[i][0]-pos[0], y=points[i][1]-pos[1];
                points[i]=[(x*Math.cos(r)+y*Math.sin(r))*100/(scale[0]||0.0001),(-x*Math.sin(r)+y*Math.cos(r))*100/(scale[1]||0.0001)];
            }
            if(!samePoints(points,last))keys.push([f,{vertices:points,closed:true},'hold']);
            last=points;
        }
        if(keys.length)set(path,{keys:keys},shape);
    }
    function shadow(layer,data) {
        if(!data) return;
        var fx=layer.property('ADBE Effect Parade').addProperty('ADBE Drop Shadow');
        var dx=data[0],dy=data[1];
        fx.property(1).setValue([85/255,85/255,85/255,1]);
        fx.property(2).setValue(data[3]*255);
        fx.property(3).setValue(Math.atan2(dx,-dy)*180/Math.PI);
        fx.property(4).setValue(Math.sqrt(dx*dx+dy*dy));fx.property(5).setValue(data[2]*2);
    }
    function createLayer(comp,d) {
        var layer;
        if (d.type==='text') layer=textLayer(comp,d);
        else if (d.type==='path') {layer=comp.layers.addShape();drawShape(layer,d);}
        else if (d.type==='image') layer=comp.layers.add(footage(d.asset));
        else throw Error('Type de calque inconnu : '+d.type);
        layer.name=d.name;
        if(d.comment)layer.comment=d.comment;
        var transform=layer.property('ADBE Transform Group');
        set(transform.property('ADBE Anchor Point'),[0,0]);
        set(transform.property('ADBE Position'),d.position || [0,0]);
        set(transform.property('ADBE Scale'),d.scale);
        set(transform.property('ADBE Rotate Z'),d.rotation);
        set(transform.property('ADBE Opacity'),d.opacity);
        layer.startTime=0;layer.inPoint=d.start/fps;layer.outPoint=d.end/fps;
        clipRect(layer,d);shadow(layer,d.dropShadow);
        return layer;
    }
    function markers(comp,items,offset) {
        for(var i=0;i<items.length;i++){
            var marker=new MarkerValue(items[i].label);
            comp.markerProperty.setValueAtTime((offset+items[i].frame)/fps,marker);
        }
    }
    function checkMedia(data) {
        for(var i=0;i<data.scenes.length;i++) {
            var s=data.scenes[i];
            if(!localFile(s.audio).exists)throw Error('Fichier manquant : '+s.audio);
            for(var j=0;j<s.layers.length;j++){
                var l=s.layers[j];
                if(l.type==='image'&&!localFile(l.asset).exists)throw Error('Image manquante : '+l.asset);
            }
        }
    }
    function create(data) {
        fps=data.fps;
        var sum=0,i,j;
        for(i=0;i<data.scenes.length;i++)sum+=data.scenes[i].frames;
        checkMedia(data);
        // After Effects presents its native save/discard dialog if a previous project has unsaved edits.
        project=app.newProject();if(!project)return;
        app.beginUndoGroup('Créer le montage Digital Lab');undoStarted=true;
        footageFolder=project.items.addFolder('Médias');
        sceneFolder=project.items.addFolder('Séquences à modifier');
        master=project.items.addComp(data.name,data.width,data.height,1,sum/fps,fps);
        master.bgColor=[1,1,1];background(master);
        var start=0;
        for(i=0;i<data.scenes.length;i++){
            var s=data.scenes[i];
            context=s.name;
            var comp=project.items.addComp(s.name,data.width,data.height,1,s.frames/fps,fps);
            comp.parentFolder=sceneFolder;comp.bgColor=[1,1,1];background(comp);
            var speech=comp.layers.add(footage(s.audio));speech.name='Voix off — '+s.name;
            speech.startTime=0;speech.inPoint=0;speech.audioEnabled=true;
            for(j=0;j<s.layers.length;j++){context=s.name+' / '+s.layers[j].name;createLayer(comp,s.layers[j]);}
            markers(comp,s.markers,0);markers(master,s.markers,start);
            var nested=master.layers.add(comp);
            nested.name=s.name;nested.startTime=start/fps;nested.inPoint=start/fps;
            start+=s.frames;nested.outPoint=start/fps;
        }
        context='référence vidéo';
        if (data.reference && localFile(data.reference).exists) {
            var guide=master.layers.add(footage(data.reference));
            guide.name='Référence MP4 · activer pour comparer';
            guide.guideLayer=true;guide.audioEnabled=false;guide.enabled=false;guide.locked=true;
        }
        master.openInViewer();
        var stem=String(data.name).replace(/[\\\/:*?"<>|]/g,'_');
        var dest=localFile(stem+'.aep'), counter=2;
        while(dest.exists) {dest=localFile(stem+' ('+(counter++)+').aep');}
        project.save(dest);
        if(!dest.exists)throw Error('Après enregistrement, le fichier .aep est introuvable.');
        return dest;
    }
    try {
        var result=create(loadData());
        if (result) alert('Projet After Effects enregistré.\n\n'+result.fsName+'\n\nOuvrez « Séquences à modifier » pour éditer une scène.');
    } catch(error) {
        alert('Création du projet interrompue.\n'+context+'\n'+error.toString()+
              (error.line ? '\nLigne '+error.line : ''));
    } finally {
        if(undoStarted)app.endUndoGroup();
    }
}());

