$(document).ready(function () {
  var conteo = 1;
  var op1 = 0;
  var op2 = 0;
  var opsign = 0;
  var modo = 1;
  var audioexiste = 0;
  let blob;
  let recorder;
  let mediaStream;
  let audio = new Audio();
  var duracion = 0;
  var colorog = "#d400e7";
  var colorpr = "#3cff6d";

  Pace.options = {
    ajax: false,
  };

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
    }
  }

  function playAudio(audioblob) {
    audio.src = URL.createObjectURL(audioblob);
    audio.play();
  }

  function validar() {
    console.log("urias");
  }

  function stopAudio() {
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
    }
  }


  function startRecording() {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(function (stream) {
        mediaStream = stream; // Guardamos la stream para su posterior uso
        recorder = RecordRTC(stream, {
          type: "audio",
          mimeType: "audio/wav",
          sampleRate: 44100,
          bufferSize: 16384,
          numberOfAudioChannels: 1,
          recorderType: RecordRTC.StereoAudioRecorder,
        });
        recorder.startRecording();
      })
      .catch(function (err) {
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
      console.error("Ninguna grabación ha sido iniciada.");
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
      beforeSend: function () {
        Pace.restart();
      },
      complete: function () {
        Pace.stop();
      },
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
      console.error("Ninguna grabación ha sido iniciada.");
      return;
    }

    recorder.stopRecording(function () {
      blob = recorder.getBlob();
      let url = URL.createObjectURL(blob);
      audio.src = url;
      audio.play();
      duracion = audio.duration * 1000;
      recorder = null;
      if (mediaStream) {
        mediaStream.getTracks().forEach((track) => track.stop());
        mediaStream = null; // Puedes ponerlo a null para asegurarte de que ya no se usará
      }
    });
  }

  function alertacorta(fuerte, debil) {
    var nuevoElemento = $(`<div class="alert alert-info ms-3 esperanza popup">
    <strong>${fuerte}</strong> ${debil}
  </div>`);
    nuevoElemento.appendTo("#alertas");
    setTimeout(function () {
      nuevoElemento.remove();
    }, 3000);
  }

  function filtrar(id, filtro) {
    poder1 = $("#p1" + id).val();
    conteo = conteo + 1;
    datos = datificar(id);
    //alert(poder1);
    const filtros = {
      1: "/filtrodel1",
      2: "/integrar",
      3: "/diferenciar",
      8: "/reflexion",
    };

    const nombres = {
      1: "filtrodel1",
      2: "integrar",
      3: "diferenciar",
      8: "reflexion",
    };


    if (filtro == 8) {
      $.ajax({
        url: filtros[filtro],
        data: { id: id, filtro: nombres[filtro], poder: poder1, idintegral: (conteo), },
        type: "POST",
        beforeSend: function () {
          Pace.restart();
        },
        complete: function () {
          Pace.stop();
        },
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
            colorog,
            ("gra" + id),
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
    } else {
      $.ajax({
        url: filtros[filtro],
        data: { id: id, filtro: nombres[filtro], poder: poder1, idintegral: (conteo) },
        type: "POST",
        beforeSend: function () {
          Pace.restart();
        },
        complete: function () {
          Pace.stop();
        },
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

          agregarElemento(conteo, 100, (conteo + "- " + "Resultado"));
          cambiarmodo(modo);
          identificar(
            "/static/data/" + conteo + ".csv",
            colorog,
            ("gra" + conteo),
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


  }

  function actualizar(numero) {
    let datos = datificar(numero);
    $.ajax({
      url: "/datos",
      data: datos,
      type: "POST",
      beforeSend: function () {
        Pace.restart();
      },
      complete: function () {
        Pace.stop();
      },
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

  function actualizar2(numero) {
    let datos2 = datificar2(numero);
    let datos = datificar(numero);
    $.ajax({
      url: "/cortito",
      data: datos2,
      type: "POST",
      beforeSend: function () {
        Pace.restart();
      },
      complete: function () {
        Pace.stop();
      },
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

  function actualizar6(numero) {
    let datos2 = datificar3(numero);
    let datos = datificar(numero);
    $.ajax({
      url: "/practica5",
      data: datos2,
      type: "POST",
      beforeSend: function () {
        Pace.restart();
      },
      complete: function () {
        Pace.stop();
      },
      success: function (response) {
        var urls = ["/static/data/" + (numero + "a.csv"), "/static/data/" + (numero + "b.csv"), "/static/data/" + (numero + "c.csv")];
        var colores = ["#afafaf", "#31be0a", "#d400e7"];
        identificartriple(
          urls,
          colores,
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

  function datificar(numero) {
    var amplitudid = "#da" + numero;
    var amplitudrealid = "#a" + numero;
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
      amplitudreal: $(amplitudrealid).val(),
      frecuencia: $(frecid).val(),
      muestration: $(muesid).val(),
      periodo: $(frecid).val(),
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
    };
  }

  function datificar2(numero) {
    var dest = "gra" + numero;
    var tipoid = "#update" + numero;
    var esc_tiempoid = "#n" + numero;
    var reflexionid = "#o" + numero;
    var corrimientoid = "#p" + numero;

    return {
      destino: dest,
      tipo: $(tipoid).attr("data-tipo"),
      id: numero,
      esc_tiempo: $(esc_tiempoid).val(),
      corrimiento: $(corrimientoid).val(),
    };
  }

  function datificar3(numero) {
    var dest = "gra" + numero;
    var tipoid = "#update" + numero;
    var segundosid = "#sg" + numero;
    var frecmueid = "#fm" + numero;
    var frecogid = "#fs" + numero;

    return {
      destino: dest,
      tipo: $(tipoid).attr("data-tipo"),
      id: numero,
      mue_mz: $(frecmueid).val(),
      og_mz: $(frecogid).val(),
      segundos: $(segundosid).val(),
    };
  }

  function identificartriple(urls, colores, destino, lineas, tipo) {
    var datosGrafica = [];

    function agregarDatos(url, color, callback, linesest, tipeset) {
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

          datosGrafica.push({
            x: x,
            y: y,
            mode: linesest,
            type: tipeset,
            line: {
              color: color,
              width: 4,
            },
            marker: {
              size: 0.04,
              color: '#afafaf',
              symbol: "X",
            },
            width: 0.04,
          });

          callback(); 
        }
      });
    }

    function procesarURLs(index) {
      if (index < urls.length) {
        linee = "lines"
        tipoo = "scatter"
        if (index == 0) {
          linee = "markers"
          tipoo = "bar"
        }
        agregarDatos(urls[index], colores[index], function () {
          procesarURLs(index + 1);  
        }, linee, tipoo);
      } else {
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
        // Grafica los datos cuando todos los archivos CSV se han procesado.
        Plotly.newPlot(destino, datosGrafica, layout);
      }
    }

    // Inicia el procesamiento de archivos CSV.
    procesarURLs(0);
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
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="a${N}" min="1" max="100" value="1" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='a${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imga${N}" class="text-white text-center mb-2"> 1 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="dda${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Escalamiento de amplitud
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="da${N}" min="1" max="100" value="1" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='da${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgda${N}" class="text-white text-center mb-2"> 1 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="bb${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Periodo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="b${N}" min="0.1" max="100" value="0.1" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='b${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgb${N}" class="text-white text-center mb-2"> 0.1 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="cc${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Muestreo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="c${N}" min="10" max="1000" value="1000" step="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='c${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgc${N}" class="text-white text-center mb-2"> 1000 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="dd${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Numero de periodos
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-8">
                    <input type="range" id="d${N}" min="1" max="10" value="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice">
                </div>
                <div class="col-1">
                    <h6 class="text-white text-center mb-2"> 1 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ee${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Sigma
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="e${N}" min="-1" max="1" value="-1" step="0.01"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='e${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imge${N}" class="text-white text-center mb-2"> -1 </h6>
                </div>
            </div>
        </div>
        
        <div class="container-fluid mt-5 mb-4 d-none" id="ff${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Omega
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="f${N}" min="-2" max="2" value="-2" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='f${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgf${N}" class="text-white text-center mb-2"> -2 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="gg${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Frecuencia angular
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="g${N}" min="-10" max="10" value="-10" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='g${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgg${N}" class="text-white text-center mb-2"> -10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="hh${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Angulo de fase
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="h${N}" min="-10" max="10" value="-10" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='h${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgh${N}" class="text-white text-center mb-2"> -10 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="mm${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Desplazamiento
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="m${N}" min="-10" max="10" value="0" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='m${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgm${N}" class="text-white text-center mb-2"> 0 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="nn${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Escalamiento en el tiempo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="n${N}" min="0" max="10" value="0.01" step="0.01"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='n${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgn${N}" class="text-white text-center mb-2"> 0 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ffs${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Frecuencia de señal
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="fs${N}" min="3" max="1000" value="3" step="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='fs${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgfs${N}" class="text-white text-center mb-2"> 3 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ffm${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Frecuencia de muestreo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="fm${N}" min="3" max="1000" value="6" step="1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='fm${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgfm${N}" class="text-white text-center mb-2"> 6 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ssg${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Segundos
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="sg${N}" min="0.01" max="10" value="2" step="0.01"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='sg${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgsg${N}" class="text-white text-center mb-2"> 2 </h6>
                </div>
            </div>
        </div>

        

        <div class="container-fluid mt-5 mb-4 d-none" id="pp${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Corrimiento en el tiempo
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="p${N}" min="-10" max="10" value="0" step="0.1"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='p${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgp${N}" class="text-white text-center mb-2"> 0 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ddi${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Inicio
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="di${N}" min="-100" max="100" value="-100" step="0.5"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='di${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgdi${N}" class="text-white text-center mb-2"> -100 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="ddf${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Fin
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="df${N}" min="-100" max="100" value="100" step="0.5"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='df${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgdf${N}" class="text-white text-center mb-2"> 100 </h6>
                </div>
            </div>
        </div>

        <div class="container-fluid mt-5 mb-4 d-none" id="pp1${N}">    
            <h5 class="text-white text-center mt-2 mb-4">Poder del filtro del 1
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
                <div class="col-1">
                    <h6 class="text-white text-center mb-2">  </h6>
                </div>
                <div class="col-9">
                    <input type="range" id="p1${N}" min="0.01" max="1" value="0.01" step="0.01"
                        class="form-control mi-input custom-input rounded-5 w-100 mb-2 deslice gordo" data-id='p1${N}';>
                </div>
                <div class="col-2">
                    <h6 id="imgp1${N}" class="text-white text-center mb-2"> 0.01 </h6>
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

        <div class="container-fluid mt-5 mb-4 d-none" id="oo${N}">    
            <h5 class="text-white text-center mt-2 mb-4">
            </h5>
            <div class="row d-flex align-content-center justify-content-center align-items-center ojo">
               
              <div class="col-10">corrimi
                <button  id="0${N}" class="btn btn-black text-white mi-input custom-input custom-op rounded-5 w-100 mb-2 esperanza reflexion" data-id='${N}';>
                  <div class="mb-0 ms-1 me-1"><h5 class="text-center mb-1">Reflexion
                  </h5></div>
                </button>
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
    while (i < conteo + 1) {
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
    while (i < conteo + 1) {
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
    sliders(id, 22);
    op1 = id;
    opsign = oper;
    desactivarcambios();
    var nuevoElemento =
      $(`<div id="avisomodo" class="alert alert-info ms-5 esperanza pulse fadein">
    <strong>${operaciones[opsign]}</strong> Elija la señal 2
  </div>`);
    nuevoElemento.appendTo("#alertas");
  }

  function terminarop(id) {
    deselegir(id);
    cambiarmodo(3);
    activarcambios();
    $("#avisomodo").remove();
  }

  function operar() {

    const operaciones = {
      1: "suma",
      2: "resta",
      3: "multiplicacion",
    };
    datos1 = datificar(op1);
    datos2 = datificar(op2);
    conteo = conteo + 1;

    $.ajax({
      url: "/urias",
      contentType: 'application/json',
      data: JSON.stringify({
        datosA: datos1,
        datosB: datos2,
        tipo: operaciones[opsign],
        idresultante: conteo,
      }),
      type: "POST",
      beforeSend: function () {
        Pace.restart();
      },
      complete: function () {
        Pace.stop();
      },
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
        agregarElemento(conteo, 100, (conteo + "- " + "Resultado"));
        cambiarmodo(modo);
        identificar(
          "/static/data/" + conteo + ".csv",
          colorog,
          ("gra" + conteo),
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

  function cambiarmodo(modo) {
    var i = 2;
    var cam = 1;

    while (i < conteo + 1) {
      const ids = [
        "aa", //amplitud
        "bb", //periodo
        "cc", //muestration
        "dd", // numero de periodos
        "ee", // sigma
        "ff", // omega
        "gg", // frecuencia angular
        "hh", // angulo de fase
        "ii", // colorf
        "jj", // paridad
        "kk", // forma
        "mm", // desplazamiento
        "nn", // escalamiento
        "oo", // reflexion
        "pp", // corrimiento en el tiempo
        "qq", // sumar
        "rr", // restar
        "ss", // multiplicar
        "tt", // filtro del 1
        "uu", // integrar
        "vv", // diferenciar
        "ww", // elegir
        "xx", // cancelar
        "dda", // amplitid buena
        "ddi", // inicio
        "ddf", // fin
        "pp1", // Poder del filtro del 1
      ];
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
      tipo = (i) => gettipo(i);
    } else {
      const camMapping = {
        2: 19,
        3: 20,
        4: 21,
      };

      const cam = camMapping[modo];
      if (!cam) {
        console.error(`Modo no reconocido: ${modo}`);
        return;
      }

      tipo = () => cam;
    }

    while (i < conteo + 1) {
      sliders(i, tipo(i));
      i++;
    }
  }

  function sliders(id, tipo) {
    const tipoToGraf = {
      1: 2,
      2: 2,
      3: 2,
      4: 3,
      5: 3,
      6: 4,
      7: 18,
      8: 1,
      9: 1,
      10: 1,
      11: 1,
      12: 1,
      13: 2,
      14: 101,
      15: 102,
      18: 18,
      19: 14,
      20: 15,
      21: 16,
      22: 17,
      100: 100,
    };

    const grafToIds = {
      1: ["aa", "bb", "cc", "mm", "ddi", "ddf", "ii", "jj", "kk"],
      2: ["aa", "cc", "mm", "ddi", "ddf", "ii", "jj", "kk"],
      3: ["cc", "ddi", "ddf", "ee", "ff", "ii", "jj", "kk"],
      4: ["dda", "gg", "hh", "cc", "ddi", "ddf", "ii", "jj", "kk"],
      14: ["nn", "oo", "pp", "ii"],
      15: ["dda", "qq", "rr", "ss", "uu", "pp1", "tt", "vv", "ii"],
      16: ["ww"],
      17: ["xx"],
      18: ["ddi", "ddf", "ii"],
      100: ["ii"],
      101: ["ssg", "ffm"],
      102: ["ffs", "ffm", "ssg"],
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
    var tipo = $(this).attr("data-tipo");

    if (modo == 2) {
      actualizar2(numero);
    } else {
      actualizar(numero);
    }
  });

  $(document).on("click", ".practica5", function () {
    var numero = $(this).attr("data-id");
    var tipo = $(this).attr("data-tipo");

    actualizar6(numero);

  });

  function getnombre(tipo) {
    tipoe = "";
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
      case 18:
        tipoe = "Resultado";
        break;
      case 8:
        tipoe = "Cuadrada";
        break;
      case 9:
        tipoe = "Tren de impulsos";
        break;
      case 10:
        tipoe = "Dientes de sierra";
        break;
      case 11:
        tipoe = "Triangular";
        break;
      case 12:
        tipoe = "Botar pelota";
        break;
      case 13:
        tipoe = "Impulso triangular";
        break;
      case 14:
        tipoe = "Sen(4pi * t) + Sen(8pi * t)";
        break;
      case 15:
        tipoe = "Sinusoidal pura";
        break;
    }
    return tipoe;
  }

  $(document).on("click", "#agregar", function () {
    conteo = conteo + 1;
    var destino = "gra" + conteo;
    var elec = parseInt($("#senal").val());
    var tipoe = "" + (conteo - 1) + "- " + getnombre(elec);

    if (elec == 7) {
      mandarAudio(conteo);
    }

    if (elec == 15 || elec == 14) {

      $.ajax({
        url: "/practica5",
        data: {
          tipo: elec,
          id: conteo,
          mue_mz: 3,
          og_mz: 3,
          segundos: 2,
        },
        type: "POST",
        beforeSend: function () {
          Pace.restart();
        },
        complete: function () {
          Pace.stop();
        },
        success: function (response) {
          //alert(conteo);
          agregarElemento(conteo, elec, tipoe);
          cambiarmodo(modo);
          var urls = ["/static/data/" + (conteo + "a.csv"),"/static/data/" +  (conteo + "b.csv"),"/static/data/" +  (conteo + "c.csv")];
          var colores = ["#afafaf", "#31be0a", "#d400e7"];
          identificartriple(
            urls,
            colores,
            destino,
            "lines",
            "scatter"
          );

          $("#update" + conteo).removeClass("recolector");
          $("#update" + conteo).addClass("practica5");

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

      

    } else {

      $.ajax({
        url: "/datos",
        data: {
          amplitud: 1,
          amplitudreal: 1,
          frecuencia: 1,
          muestration: 1000,
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
          inicio: -100,
          fin: 100,
        },
        type: "POST",
        beforeSend: function () {
          Pace.restart();
        },
        complete: function () {
          Pace.stop();
        },
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
    }


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
      confirmButtonText: "Pausar",
      denyButtonText: "Cancelar",
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
    nuevoElemento.appendTo("#alertas");
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
    nuevoElemento.appendTo("#alertas");
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
    nuevoElemento.appendTo("#alertas");
    setTimeout(function () {
      nuevoElemento.remove();
    }, 3000);
    cambiarmodo(3);
    modo = 3;
  });

  $(document).on("blur", ".libre", function () {
    var valor = parseFloat($(this).val());
    if (isNaN(valor) || valor < $(this).attr("min")) {
      $(this).val($(this).attr("min"));
    } else if (valor > $(this).attr("max")) {
      $(this).val($(this).attr("max"));
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

  $(document).on("click", ".reflexion", function () {
    id = $(this).attr("data-id");
    filtrar(id, 8);
  });

  $(document).on("click", ".diferenciar", function () {
    id = $(this).attr("data-id");
    filtrar(id, 3);
  });

  $(document).on("click", ".filtro1", function () {
    id = $(this).attr("data-id");
    filtrar(id, 1);
  });

  $(document).on("input", ".gordo", function () {
    id = $(this).attr("data-id");
    $("#img" + id).text($(this).val());
  });




  audio.addEventListener("loadedmetadata", function () {
    let durationInSeconds = audio.duration;
    duracion = durationInSeconds * 1000;
    console.log(duracion);
    Swal.fire({
      title: "Reproduciendo...",
      timer: duracion,
      timerProgressBar: true,
      showConfirmButton: false,
      showCancelButton: false,
      allowOutsideClick: false,
      allowEscapeKey: false,
      background: "#212529",
      color: colorpr,
    });
  });
});
