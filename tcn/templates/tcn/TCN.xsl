<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html lang="en">
          <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
            <script>

            </script>
            <title>TCN</title>
          </head>

          <body>

            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-12">
                        <h3 class="text-center">
                            时序控制参数
                        </h3>
                    </div>
                </div>
                <hr>
                 <div class="row">
                     <div class="col-md-3"></div>
                     <div class="col-md-2">
                        <div class="input-group mb-3">
                          <div class="input-group-prepend">
                            <span class="input-group-text" id="basic-addon1">Version:</span>
                          </div>
                          <input type="text" class="form-control"  aria-describedby="basic-addon1"  readonly="true" value="V11">
                        </div>
                     </div>
                     <div class="col-md-2">
                         <div class="input-group mb-3">
                              <div class="input-group-prepend">
                                <span class="input-group-text" id="basic-addon1">Operator:</span>
                              </div>
                              <input type="text" class="form-control"  aria-describedby="basic-addon1"  readonly="true" value="hunter">
                        </div>
                     </div>
                     <div class="col-md-2">
                         <div class="input-group mb-3">
                              <div class="input-group-prepend">
                                <span class="input-group-text" id="basic-addon1">ShotNum:</span>
                              </div>
                              <input type="text" class="form-control"  aria-describedby="basic-addon1" readonly="true" value="20030">
                        </div>
                     </div>
                     <div class="col-md-3"></div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-md-2" align="center">

                        <button type="button" class="btn btn-success btn-md " style="width: 70%">
                            ECRH245GC
                        </button>
                        <hr>
                    </div>
                    <div class="col-md-10">
                        <div class="row">
                            <div class="col-md-3">
                        <form role="form">
                            <div class="form-row "><h4 style="text-align: center">BasicInformation</h4></div>
                            <div class="form-row">
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        Name:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        Id:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-12">

                                    <label for="exampleInputEmail1">
                                        InitValue:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-12">

                                    <label for="exampleInputEmail1">
                                        TimeUnit:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>

                            </div>
                        </form>

        {#                <form role="form">#}
        {#                    <div class="form-group">#}
        {##}
        {#                        <label for="exampleInputEmail1">#}
        {#                            Email address#}
        {#                        </label>#}
        {#                        <input type="email" class="form-control" id="exampleInputEmail1" />#}
        {#                    </div>#}
        {#                    <div class="form-group">#}
        {##}
        {#                        <label for="exampleInputPassword1">#}
        {#                            Password#}
        {#                        </label>#}
        {#                        <input type="password" class="form-control" id="exampleInputPassword1" />#}
        {#                    </div>#}
        {#                </form>#}
                    </div>
                            <div class="col-md-3">
                        <form role="form">
                            <div class="form-row "><h4 style="text-align: center">AttachedInformation</h4></div>
                            <div class="form-row">
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        Division:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-6">

                                    <label for="exampleInputPassword1">
                                        PersonInCharge:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputPassword1" />
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        ToPosition:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-6">

                                    <label for="exampleInputPassword1">
                                        InsituPosition
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputPassword1" />
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        CreatedDate:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-6">

                                    <label for="exampleInputPassword1">
                                        Comment:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputPassword1" />
                                </div>
                            </div>
                        </form>
                    </div>
                            <div class="col-md-3">
                                <form role="form">
                                    <div class="form-row "><h4 style="text-align: center">TriggerCondition</h4></div>
                                    <div class="form-row">
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputEmail1">
                                                IsSgmInv:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputEmail1" />
                                        </div>
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputPassword1">
                                                OrSignal:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputPassword1" />
                                        </div>
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputPassword1">
                                                AndSignal:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputPassword1" />
                                        </div>
                                    </div>
                                    <div class="form-row">
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputEmail1">
                                                IsInverse:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputEmail1" />
                                        </div>
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputPassword1">
                                                AndSgm:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputPassword1" />
                                        </div>
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputPassword1">
                                                CtnsSgm1:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputPassword1" />
                                        </div>
                                    </div>
                                    <div class="form-row">
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputEmail1">
                                                IsProtection:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputEmail1" />
                                        </div>
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputPassword1">
                                                DelayTime:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputPassword1" />
                                        </div>
                                        <div class="form-group col-md-4">

                                            <label for="exampleInputPassword1">
                                                NoUse:
                                            </label>
                                            <input type="text" class="form-control" id="exampleInputPassword1" />
                                        </div>
                                    </div>
                                </form>
                            </div>
                            <div class="col-md-3">
                        <form role="form">
                            <div class="form-row "><h4 style="text-align: center">PhaseClass</h4></div>
                            <div class="form-row">
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        RepeatNumber:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-6">

                                    <label for="exampleInputPassword1">
                                        TimingMode:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputPassword1" />
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-6">

                                    <label for="exampleInputEmail1">
                                        StartTime:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                                <div class="form-group col-md-6">

                                    <label for="exampleInputPassword1">
                                        LowWidth
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputPassword1" />
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group col-md-12">

                                    <label for="exampleInputEmail1">
                                        HighWidth:
                                    </label>
                                    <input type="text" class="form-control" id="exampleInputEmail1" />
                                </div>
                            </div>
                        </form>
                    </div>
                        </div>


                    </div>

                </div>

            </div>
            <!-- Optional JavaScript -->
            <!-- jQuery first, then Popper.js, then Bootstrap JS -->
            <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
          </body>

        </html>
    </xsl:template>
</xsl:stylesheet>