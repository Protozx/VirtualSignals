$(document).ready(function () {
  var conteo = 1;
  var op1 = 0;
  var op2 = 0;
  var opsign = 0;
  var modo = 1;
  var audioexiste = 0;
  let blob;
  let recorder;
  let audio = new Audio();
  var duracion = 0;
  var colorog = "#d400e7";
  var colorpr = "#3cff6d";


  $("#ingresarh").click(function () {
    window.location.href = "login.php";
  });

  nombre = "Melanie";
  //sliders(1,1);
  //identificar("/static/data/g1.csv", "#00FFFB", "gra1", "lines", "scatter");

  $("#per").text(nombre);

  function gettipo(numero) {
    var tipoid = "#update" + numero;
    return $(tipoid).attr("data-tipo");
  }
  function activaraudio() {
    if (audioexiste == 0) {
      $("#senal").append(`<option value="7">Voz humana</option>`);
      audioexiste = 1;

    };
  }

  function playAudio(audioblob) {
    audio.src = URL.createObjectURL(audioblob);
    audio.play();
  }

  function stopAudio() {
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
    }
  }

  function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      recorder = RecordRTC(stream, {
        type: 'audio',
        mimeType: 'audio/wav',
        sampleRate: 44100,
        bufferSize: 16384,
        numberOfAudioChannels: 1,
        recorderType: RecordRTC.StereoAudioRecorder
      });
      recorder.startRecording();
    }).catch(function (err) {
      Swal.close();
      Swal.fire({
        title: "Error al obtener acceso al microfono!",
        confirmButtonColor: colorpr,
        background: "#212529",
        color: "#ffffff",
        iconColor: colorpr,
        icon: "error",
        confirmButtonText: "Ok",
      });
    });
  }


  function stopAndStoreRecording() {
    if (!recorder) {
      console.error('Ninguna grabación ha sido iniciada.');
      return;
    }

    recorder.stopRecording(function () {
      blob = recorder.getBlob();
      audiosArray.push(blob);
      recorder.stream.stop();
      recorder = null;
    });
  }

  function mandarAudio(id) {
    var formData = new FormData();
    formData.append("id", id);
    formData.append("audio", blob);
    
    $.ajax({
      url: "/audio",
      data: formData,
      type: "POST",
      processData: false,  
      contentType: false,
      success: function (response) {
        Swal.fire({
          title: "Audio generado!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "success",
          confirmButtonText: "Ok",
        });

      },
      error: function (error) {
        Swal.fire({
          title: "Error ocurrido!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "error",
          confirmButtonText: "Ok",
        });
      },
    });
  }

  function stopAndPlayRecording() {
    if (!recorder) {
      console.error('Ninguna grabación ha sido iniciada.');
      return;
    }

    recorder.stopRecording(function () {
      blob = recorder.getBlob();
      let url = URL.createObjectURL(blob);
      audio.src = url;
      audio.play();
      duracion = audio.duration * 1000;
      recorder.stream.stop();
      recorder = null;
    });
  }

  function alertacorta(fuerte, debil) {
    var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
    <strong>${fuerte}</strong> ${debil}
  </div>`);
    nuevoElemento.appendTo('#alertas');
    setTimeout(function () {
      nuevoElemento.remove();
    }, 3000);
  }

  function filtrar(id, filtro) {
    datos = datificar(id);
    const filtros = {
      1: "/filtrodel1",
      2: "/integrar",
      3: "/diferenciar",
    };

    $.ajax({
      url: filtros[filtro],
      data: { id: id, filtro: filtro },
      type: "POST",
      success: function (response) {
        Swal.fire({
          title: "Transfomacion realizada!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "success",
          confirmButtonText: "Ok",
        });

        identificar(
          "/static/data/" + id + ".csv",
          datos.color,
          datos.destino,
          "lines",
          "scatter"
        );

      },
      error: function (error) {
        Swal.fire({
          title: "Error ocurrido!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "error",
          confirmButtonText: "Ok",
        });
      },
    });


  }

  function actualizar(numero) {
    let datos = datificar(numero);
    $.ajax({
      url: "/datos",
      data: datos,
      type: "POST",
      success: function (response) {
        if (datos.continuidad == 0) {
          identificar(
            "/static/data/" + numero + ".csv",
            datos.color,
            datos.destino,
            "lines",
            "scatter"
          );
        } else {
          identificar(
            "/static/data/" + numero + ".csv",
            datos.color,
            datos.destino,
            "markers",
            "bar"
          );
        }
      },
      error: function (error) {
        Swal.fire({
          title: "Error ocurrido!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "error",
          confirmButtonText: "Ok",
        });
      },
    });

  }

  function datificar(numero) {
    var amplitudid = "#da" + numero;
    var frecid = "#b" + numero;
    var muesid = "#c" + numero;
    var perioid = "#d" + numero;
    var colorid = "#i" + numero;
    var parid = "#j" + numero;
    var contid = "#k" + numero;
    var sigmaid = "#e" + numero;
    var omegaid = "#f" + numero;
    var frec_angid = "#g" + numero;
    var ang_faseid = "#h" + numero;
    var desplaid = "#m" + numero;
    var dest = "gra" + numero;
    var tipoid = "#update" + numero;
    var esc_tiempoid = "#n" + numero;
    var reflexionid = "#o" + numero;
    var corrimientoid = "#p" + numero;
    var inicioid = "#di" + numero;
    var finid = "#df" + numero;

    return {
      amplitud: $(amplitudid).val(),
      frecuencia: $(frecid).val(),
      muestration: $(muesid).val(),
      periodo: $(perioid).val(),
      sigma: $(sigmaid).val(),
      omega: $(omegaid).val(),
      frecuencia_angular: $(frec_angid).val(),
      angulo_fase: $(ang_faseid).val(),
      color: $(colorid).val(),
      desplazamiento: $(desplaid).val(),
      par: $(parid).val(),
      continuidad: $(contid).val(),
      destino: dest,
      tipo: $(tipoid).attr("data-tipo"),
      id: numero,
      esc_tiempo: $(esc_tiempoid).val(),
      reflexion: $(reflexionid).val(),
      corrimiento: $(corrimientoid).val(),
      inicio: $(inicioid).val(),
      fin: $(finid).val(),
    }
  }

  function identificar(url, primario, destino, lineas, tipo) {
    Papa.parse(url, {
      download: true,
      header: true,
      dynamicTyping: true,
      complete: function (results) {
        var x = [];
        var y = [];
        results.data.forEach(function (dato) {
          x.push(dato.x);
          y.push(dato.y);
        });
        var datosGrafica = [
          {
            x: x,
            y: y,
            mode: lineas,
            type: tipo,
            line: {
              color: primario,
              width: 4,
            },
            marker: {
              size: 10,
              color: primario,
              symbol: "o",
            },
            width: 0.04,
          },
        ];
        var layout = {
          title: "",
          showlegend: false,
          autosize: true,
          plot_bgcolor: "#000000",
          paper_bgcolor: "#000000",
          xaxis: {
            rangeslider: {},
            color: "#FFFFFF",
            gridcolor: "#888888",
          },
          yaxis: {
            fixedrange: true,
            color: "#FFFFFF",
            gridcolor: "#888888",
          },
        };

        Plotly.newPlot(destino, datosGrafica, layout);
      },
    });
  }

  function agregarElemento(N, T, nombre) {
    let nuevoElemento = `<div class="row bg-dark shadow-sm rounded-5 d-flex align-content-center justify-content-center align-items-center mt-5 mb-5 fadein" id="chunche${N}">

                                                

    <div class="col-4 flex-column justify-content-center mt-2 mb-3">
        
        
        <div class="container-fluid mt-5 mb-4 d-none" id="aa${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Amplitud
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="a${N}" min="1" max="100" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 100 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="dda${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Amplitud
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="number" id="da${N}" min="1" max="1000" step="1" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 libre">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1000 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="bb${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Frecuencia
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="b${N}" min="1" max="100" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 100 </h6>pr1nt
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="cc${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Muestreo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 10 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="c${N}" min="10" max="1000" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 900 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="dd${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Periodo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="d${N}" min="1" max="10" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ee${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Sigma
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> -1 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="e${N}" min="-100" max="100" value="0"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ff${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Omega
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> -2 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="f${N}" min="-200" max="200" value="0"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 2 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="gg${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Frecuencia angular
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 0 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="g${N}" min="0" max="10" value="0"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="hh${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Angulo de fase
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 0 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="h${N}" min="0" max="10" value="0"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="mm${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Desplazamiento
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> -10 </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="m${N}" min="-10" max="10" value="0"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="nn${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Escalamiento en el tiempo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="number" id="n${N}" min="1" max="100" step="0.01" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 libre">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 100 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="oo${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Reflexion
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="number" id="o${N}" min="1" max="10" step="1" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 libre">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="pp${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Corrimiento en el tiempo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
                <div class="col-8">
                    <input type="number" id="p${N}" min="1" max="100" step="0.1" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 libre">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 100 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ddi${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Inicio
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1% </h6>
                </div>
                <div class="col-8">
                    <input type="number" id="di${N}" min="1" max="50" step="0.1" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 libre">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 50% </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ddf${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Fin
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 51% </h6>
                </div>
                <div class="col-8">
                    <input type="number" id="df${N}" min="51" max="100" step="0.1" value="100"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 libre">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 100% </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="qq${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="q${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza operar" data-op='1' data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Sumar
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="rr${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="r${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza operar" data-op='2' data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Restar
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ss${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="s${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza operar" data-op='3' data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Multiplicar
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="tt${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="t${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza filtro1" data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Filtro del 1
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="uu${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="u${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza integrar" data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Integrar
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="vv${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="v${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza diferenciar" data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Diferenciar
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ww${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="w${N}" class="btn btn-primary text-white mi-input rounded-5 w-100 mb-2 esperanza operar2" data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Elegir
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="xx${N}">    
            
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                
                <div class="col-10">
                  <button  id="x${N}" class="btn btn-danger text-white mi-input rounded-5 w-100 mb-2 esperanza desoperar" data-id='${N}';>
                    <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Cancelar
                    </h5></div>
                  </button>
                </div>
                
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ii${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Color
            </h5>
            <input type="color" id="i${N}" value="${colorog}"
                        class="form-control mi-input custom-input rounded-5 mb-2 ojo">
        </div>

        <div class="container-fluid mt-5 mb-3 d-none" id="jj${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Paridad
            </h5>
            <select class="form-select mi-input custom-input rounded-5 w-100 ojo" id="j${N}">
                <option value="0"> Normal </option>
                <option value="1"> Par </option>
                <option value="2"> Impar </option>
            </select>
        </div>

        <div class="container-fluid mt-4 mb-3 d-none" id="kk${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Forma
            </h5>
            <select class="form-select mi-input custom-input rounded-5 w-100 ojo" id="k${N}">
                <option value="0"> Continua </option>
                <option value="1"> Discreta </option>
            </select>
        </div>


                        
                
    </div>


    <div class="col-8 flex-column justify-content-center mt-2 mb-3">

        <div class="container-fluid mt-5 mb-5">    
            <h2 class="text-white text-center mt-2 mb-4">${nombre}
            </h2>
        </div>


        <div id="gra${N}" class="rounded-5 mt-5 mb-5 ms-3 me-5 ojo"></div>

        <div class="row d-flex align-content-center justify-content-center align-items-center">
                

            <div class="col-5 mt-2 mb-2 d-flex h-100 align-items-center justify-content-end">  
            <i
                    class="fa-solid fa-rotate fa-3x px-4 rounded-4 iblanco actualizar recolector"
                    data-id='${N}';
                    data-tipo='${T}';
                    data-nombre='${nombre}';
                    id="update${N}">
                </i>
            </div>
            <div class="col-5 mt-2 mb-2 d-flex h-100 align-items-center justify-content-start">
                <i
                    class="fa-solid fa-bomb fa-3x px-4 rounded-4 iblanco eliminar"
                    data-id='${N}';
                    id="delete${N}">
                </i>
            </div>

        </div>

        

    </div>


          


</div>`;

    $("#tablon").append(nuevoElemento);
  }

  function elegir(id) {
    $("#chunche" + id).removeClass("bg-dark");
    $("#chunche" + id).addClass("bg-info");
  }

  function deselegir(id) {
    $("#chunche" + id).removeClass("bg-info");
    $("#chunche" + id).addClass("bg-dark");
  }

  function desactivarcambios() {
    var i = 2;
    while (i < (conteo + 1)) {
      const ids = ["delete", "update"];
      for (const idPrefix of ids) {
        const element = $("#" + idPrefix + i);
        if (!element.hasClass("d-none")) {
          element.addClass("d-none");
        }
      }
      i++;
    }

    $("#modo1").addClass("d-none");
    $("#modo2").addClass("d-none");
    $("#modo3").addClass("d-none");
    $("#extra").addClass("d-none");

  }

  function activarcambios() {
    var i = 2;
    while (i < (conteo + 1)) {
      const ids = ["delete", "update"];
      for (const idPrefix of ids) {
        const element = $("#" + idPrefix + i);
        if (element.hasClass("d-none")) {
          element.removeClass("d-none");
        }
      }
      i++;
    }

    $("#modo1").removeClass("d-none");
    $("#modo2").removeClass("d-none");
    $("#modo3").removeClass("d-none");
    $("#extra").removeClass("d-none");

  }

  function iniciarop(id, oper) {
    const operaciones = {
      1: "Sumando!",
      2: "Restando!",
      3: "Multiplicando!",
    };
    elegir(id);
    cambiarmodo(4);
    $("#ww" + id).addClass("d-none");
    sliders(id, 14);
    op1 = id;
    opsign = oper;
    desactivarcambios();
    var nuevoElemento = $(`<div id="avisomodo" class="alert alert-info ms-5 esperanza pulse fadein">
    <strong>${operaciones[opsign]}</strong> Elija la señal 2
  </div>`);
    nuevoElemento.appendTo('#alertas');
  }

  function terminarop(id) {
    deselegir(id)
    cambiarmodo(3);
    activarcambios();
    $("#avisomodo").remove();
  }

  function operar() {

    const operaciones = {
      1: "Suma",
      2: "Resta",
      3: "Multiplicación",
    };

    $.ajax({
      url: "/urias",
      data: {
        nombre: operaciones[opsign],
        tipo: opsign,
        id1: op1,
        id2: op2,
      },
      type: "POST",
      success: function (response) {
        Swal.fire({
          title: "Operación realizada!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "success",
          button: "Aceptar",
        });
      },
      error: function (error) {
        Swal.fire({
          title: "Error ocurrido!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "error",
          confirmButtonText: "Ok",
        });
      },
    });

  }

  function cambiarmodo(modo) {
    var i = 2;
    var cam = 1;

    while (i < (conteo + 1)) {
      const ids = ["aa", "bb", "cc", "dd", "ee", "ff", "gg", "hh", "ii", "jj", "kk", "mm", "nn", "oo", "pp", "qq", "rr", "ss", "tt", "uu", "vv", "ww", "xx", "dda", "ddi", "ddf"];
      for (const idPrefix of ids) {
        const element = $("#" + idPrefix + i);
        if (!element.hasClass("d-none")) {
          element.addClass("d-none");
        }
      }
      i++;
    }

    i = 2;

    let tipo;

    if (modo == 1) {
      tipo = i => gettipo(i);
    } else {
      const camMapping = {
        2: 11,
        3: 12,
        4: 13,
      };

      const cam = camMapping[modo];
      if (!cam) {
        console.error(`Modo no reconocido: ${modo}`);
        return;
      }

      tipo = () => cam;
    }

    while (i < (conteo + 1)) {
      sliders(i, tipo(i));
      i++;
    }


  }

  function sliders(id, tipo) {
    const tipoToGraf = {
      1: 1,
      2: 1,
      3: 1,
      4: 2,
      5: 2,
      6: 3,
      7: 8,
      8: 8,
      11: 4,
      12: 5,
      13: 6,
      14: 7,
    };

    const grafToIds = {
      1: ["dda", "bb", "cc", "dd", "mm", "ii", "jj", "kk"],
      2: ["ee", "ff", "cc", "ii", "jj", "kk"],
      3: ["aa", "gg", "hh", "cc", "ii", "jj", "kk"],
      4: ["nn", "oo", "pp", "ii"],
      5: ["dda", "qq", "rr", "ss", "tt", "uu", "vv", "ii"],
      6: ["ww"],
      7: ["xx"],
      8: ["ddi", "ddf", "ii"]
    };

    const graf = tipoToGraf[tipo];

    if (graf) {
      for (const prefix of grafToIds[graf]) {
        $("#" + prefix + id).removeClass("d-none");
      }
    }
  }





  $(document).on("click", ".recolector", function () {
    var numero = $(this).attr("data-id");
    actualizar(numero);
  });

  function getnombre(tipo) {
    tipoe = ""
    switch (tipo) {
      case 1:
        tipoe = "Escalon Unitario";
        break;
      case 2:
        tipoe = "Impulso Unitario";
        break;
      case 3:
        tipoe = "Rampa";
        break;
      case 4:
        tipoe = "Exponencial real";
        break;
      case 5:
        tipoe = "Exponencial compleja";
        break;
      case 6:
        tipoe = "Senoidal";
        break;
      case 7:
        tipoe = "Audio";
        break;
      case 8:
        tipoe = "Resultado";
        break;
    }
    return tipoe
  }

  $(document).on("click", "#agregar", function () {
    conteo = conteo + 1;
    var destino = "gra" + conteo;
    var elec = parseInt($("#senal").val());
    var tipoe = "" + (conteo - 1) + "- " + getnombre(elec);

    if (elec == 7) {
      mandarAudio(conteo);
    }

    $.ajax({
      url: "/datos",
      data: {
        amplitud: 1,
        frecuencia: 1,
        muestration: 10,
        periodo: 1,
        sigma: 0,
        omega: 0,
        frecuencia_angular: 0,
        angulo_fase: 0,
        desplazamiento: 0,
        par: 0,
        continuidad: 0,
        tipo: elec,
        id: conteo,
        esc_tiempo: 0,
        reflexion: 0,
        corrimiento: 0,
        inicio: 1,
        fin: 100,
      },
      type: "POST",
      success: function (response) {
        //alert(conteo);
        agregarElemento(conteo, elec, tipoe);
        cambiarmodo(modo);
        identificar(
          "/static/data/" + conteo + ".csv",
          colorog,
          destino,
          "lines",
          "scatter"
        );
      },
      error: function (error) {
        Swal.fire({
          title: "Error ocurrido!",
          confirmButtonColor: colorpr,
          background: "#212529",
          color: "#ffffff",
          iconColor: colorpr,
          icon: "error",
          confirmButtonText: "Ok",
        });
      },
    });
  });

  $(document)
    .on("mouseenter", ".pulsblue", function () {
      $(this).addClass("btn-primary pulse");
    })
    .on("mouseleave", ".pulsblue", function () {
      $(this).removeClass("btn-primary pulse");
    });

  $(document)
    .on("mouseenter", ".pulsred", function () {
      $(this).removeClass("btn-secondary");
      $(this).addClass("btn-danger text-white pulse");
    })
    .on("mouseleave", ".pulsred", function () {
      $(this).removeClass("btn-danger text-white pulse");
      $(this).addClass("btn-secondary");
    });

  $(document)
    .on("mouseenter", ".pulscyan", function () {
      $(this).removeClass("btn-secondary");
      $(this).addClass("btn-primary text-white pulse");
    })
    .on("mouseleave", ".pulscyan", function () {
      $(this).removeClass("btn-primary text-white pulse");
      $(this).addClass("btn-secondary");
    });

  $(document)
    .on("mouseenter", ".pulsgreen", function () {
      $(this).removeClass("btn-dark text-white");
      $(this).addClass("btn-info text-black pulse");
    })
    .on("mouseleave", ".pulsgreen", function () {
      $(this).removeClass("btn-info text-black pulse");
      $(this).addClass("btn-dark text-white");
    });

  $(document)
    .on("mouseenter", ".actualizar", function () {
      $(this).removeClass("iblanco");
      $(this).addClass("iazul pulse spin");
    })
    .on("mouseleave", ".actualizar", function () {
      $(this).removeClass("iazul pulse spin");
      $(this).addClass("iblanco");
    });

  $(document)
    .on("mouseenter", ".eliminar", function () {
      $(this).removeClass("iblanco");
      $(this).addClass("irojo pulse");
    })
    .on("mouseleave", ".eliminar", function () {
      $(this).removeClass("irojo pulse");
      $(this).addClass("iblanco");
    });

  $(document).on("mouseenter", ".ojo", function () {
    $(this).addClass("big");
  });

  $(document).on("mouseleave", ".ojo", function () {
    $(this).removeClass("big");
  });

  $(document).on("click", ".eliminar", function () {
    var numero = $(this).attr("data-id");
    $("#chunche" + numero).addClass("d-none");
  });

  $(document).on("click", "#grabar", function () {
    startRecording();
    Swal.fire({
      title: "Grabando...",
      iconColor: colorpr,
      icon: "warning",
      confirmButtonColor: colorpr,
      background: "#212529",
      color: "#ffffff",
      showDenyButton: true,
      showCancelButton: false,
      confirmButtonText: 'Pausar',
      denyButtonText: 'Cancelar',
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        stopAndPlayRecording();
        activaraudio();
        console.log(duracion);


      } else if (result.isDenied) {

      }
    });

  });

  $(document).on("click", "#modo1", function () {
    var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
    <strong>Modo 1</strong> Sliders generales
  </div>`);
    nuevoElemento.appendTo('#alertas');
    setTimeout(function () {
      nuevoElemento.remove();
    }, 3000);
    cambiarmodo(1);
    modo = 1;
  });

  $(document).on("click", "#modo2", function () {
    var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
    <strong>Modo 2</strong> Variable dependiente
  </div>`);
    nuevoElemento.appendTo('#alertas');
    setTimeout(function () {
      nuevoElemento.remove();
    }, 3000);
    cambiarmodo(2);
    modo = 2;
  });


  $(document).on("click", "#modo3", function () {
    var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
    <strong>Modo 3</strong> Variable independiente
  </div>`);
    nuevoElemento.appendTo('#alertas');
    setTimeout(function () {
      nuevoElemento.remove();
    }, 3000);
    cambiarmodo(3);
    modo = 3;
  });

  $(document).on("blur", ".libre", function () {
    var valor = parseFloat($(this).val());
    if (isNaN(valor) || valor < $(this).attr('min')) {
      $(this).val($(this).attr('min'));
    } else if (valor > $(this).attr('max')) {
      $(this).val($(this).attr('max'));
    }
  });

  $(document).on("click", ".operar", function () {
    iniciarop($(this).attr("data-id"), $(this).attr("data-op"));
  });

  $(document).on("click", ".operar2", function () {
    op2 = $(this).attr("data-id");
    operar();
    terminarop(op1);
  });

  $(document).on("click", ".desoperar", function () {
    terminarop($(this).attr("data-id"));
  });

  $(document).on("click", ".integrar", function () {
    id = $(this).attr("data-id");
    filtrar(id, 2);
  });

  $(document).on("click", ".diferenciar", function () {
    id = $(this).attr("data-id");
    filtrar(id, 3);
  });

  $(document).on("click", ".filtro1", function () {
    id = $(this).attr("data-id");
    filtrar(id, 1);
  });



  audio.addEventListener('loadedmetadata', function () {
    let durationInSeconds = audio.duration;
    duracion = durationInSeconds * 1000;
    console.log(duracion);
    Swal.fire({
      title: "Reproduciendo...",
      timer: duracion,
      timerProgressBar: true,
      showConfirmButton: false, // Oculta el botón de confirmación
      showCancelButton: false,  // Oculta el botón de cancelación
      allowOutsideClick: false, // No permite cerrar la alerta haciendo clic fuera de ella
      allowEscapeKey: false,
      background: "#212529",
      color: colorpr,

    });
  });






});
