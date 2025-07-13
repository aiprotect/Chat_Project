<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <title>Chaton Template | Themesdesign</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Premium Bootstrap v5.3.0-alpha1 Landing Page Template" />
    <meta name="keywords" content="bootstrap v5.3.0-alpha1, premium, marketing, multipurpose" />
    <meta content="Themesdesign" name="author" />

    <!-- favicon -->
    <link rel="shortcut icon" href="images/favicon.ico" />

    <!-- Bootstrap css -->
    <link href="css/bootstrap.min.css" rel="stylesheet" type="text/css" />

    <!-- Unicon Css -->
    <link href="css/bootstrap-icons.css" rel="stylesheet" type="text/css" />

    <!-- Custom Css -->
    <link href="css/style.min.css" rel="stylesheet" type="text/css" />

</head>

<body data-bs-spy="scroll" data-bs-target=".navbar" data-bs-offset="51">

    <!--Navbar Start-->
    <nav class="navbar navbar-expand-lg fixed-top sticky" id="navbar">
        <div class="container">
            <!-- LOGO -->
            <a class="navbar-brand logo text-uppercase" target="_blank" href="https://1.envato.market/themesdesign" >
                <img src="images/logo-light.png" class="logo-light" alt="logo-light" height="28">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse"
                aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
                <i class="bi bi-list text-white"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <ul class="navbar-nav ms-auto navbar-center">
                    <li class="nav-item">
                        <a href="#home" class="nav-link">Home</a>
                    </li>
                    <li class="nav-item">
                        <a href="#demos" class="nav-link">Demos</a>
                    </li>
                    <li class="nav-item">
                        <a href="#layouts" class="nav-link">Layouts</a>
                    </li>
                    <li class="nav-item">
                        <a href="#features" class="nav-link">Features</a>
                    </li>
                    <li class="nav-item">
                        <a href="#contact" class="nav-link">Contact</a>
                    </li>
                </ul>
            </div>
            <!--end navabar-collapse-->
        </div>
        <!--end container-->
    </nav>
    <!-- Navbar End -->

    <!-- START HOME -->
    <section class="bg-home2" id="home">
        <div class="bg-overlay"></div>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-7">
                    <div class="text-center">
                        <h1 class="text-white mb-4"> Chaton - HTML Chat App Template</h1>
                        <div class="badge bg-danger fs-15 mb-3">Version v1.0.0</div>
                        <p class="text-white-50 fs-17">Chaton is built with <span class="fw-semibold">Bootstrap
                                v5.3.0</span> in HTML, SCSS with responsive
                            in all devices and supported Dark, Light, RTL modes.</p>

                        <div class="mt-4 pt-2">
                            <a href="docs/html/index.html" target="_blank" class="btn btn-success ms-2">Documentation</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- START SHAPE -->
    <div class="position-relative">
        <div class="shape">
            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink"
                width="1440" height="150" preserveAspectRatio="none" viewBox="0 0 1440 150">
                <g mask="url(&quot;#SvgjsMask1022&quot;)" fill="none">
                    <path d="M 0,58 C 144,73 432,131.8 720,133 C 1008,134.2 1296,77.8 1440,64L1440 250L0 250z"
                        fill="rgba(255, 255, 255, 1)"></path>
                </g>
                <defs>
                    <mask id="SvgjsMask1022">
                        <rect width="1440" height="250" fill="#ffffff"></rect>
                    </mask>
                </defs>
            </svg>
        </div>
    </div>
    <!-- END SHAPE -->

    <!-- START FEATURE -->
    <div class="container">
        <div class="bg-feature">
            <div class="row justify-content-center">
                <div class="col-lg-6 col-md-6">
                    <div class="mt-5">
                        <img src="images/logo/bootstrap.png" alt="" height="60" class="rounded shadow mx-1 my-2">
                        <img src="images/logo/html5.png" alt="" height="60" class="rounded shadow mx-1 my-2">
                        <img src="images/logo/css3.png" alt="" height="60" class="rounded shadow mx-1 my-2">
                        <img src="images/logo/sass.png" alt="" height="60" class="rounded shadow mx-1 my-2">
                        <img src="images/logo/gulp.png" alt="" height="60" class="rounded shadow mx-1 my-2">
                        <img src="images/logo/yarn.png" alt="" height="60" class="rounded shadow mx-1 my-2">
                    </div>
                </div>
                <!--end col-->
            </div>
            <!--end row-->
        </div>
        <!--end bg-feature-->
    </div>
    <!--end container-->
    <!-- END FEATURE -->

    <!-- START SERVICE -->
    <section class="section" id="demos">
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-lg-7">
                    <div class="header-title text-center">
                        <h3>Default Demos</h3>
                        <div class="title-border mt-3"></div>
                        <p class="text-muted mt-3">Chaton is an Chat App template that is a beautifully crafted,
                            clean & minimal designed Chat App template with Dark, Light Layouts with RTL options.</p>
                    </div>
                </div>
                <!--end col-->
            </div>
            <!--end row-->

            <div class="row justify-content-center px-5">
                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/index.html" target="_blank">
                            <img src="images/demo/default.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h5 class="fs-17 mt-4">Default Light</h5>
                    </div>
                </div>
                <!-- end col -->
                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/index-dark.html" target="_blank">
                            <img src="images/demo/default-dark.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Defualt Dark </h4>
                    </div>
                </div>
                <!-- end col -->
                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/index-rtl.html" target="_blank">
                            <img src="images/demo/default-rtl.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Default RTL</h4>
                    </div>
                </div>
                <!-- end col -->

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/auth-register.html" target="_blank">
                            <img src="images/demo/signup.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Sign Up</h4>
                    </div>
                </div>
                <!-- end col -->

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/auth-login.html" target="_blank">
                            <img src="images/demo/login.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Sign In</h4>
                    </div>
                </div>
                <!-- end col -->

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/auth-recoverpw.html" target="_blank">
                            <img src="images/demo/recoverpassword.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Recover Password</h4>
                    </div>
                </div>
                <!-- end col -->

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/auth-changepassword.html" target="_blank">
                            <img src="images/demo/changepassword.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Change Password</h4>
                    </div>
                </div>
                <!-- end col -->

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/auth-lock-screen.html" target="_blank">
                            <img src="images/demo/lockscreen.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Lock Screen</h4>
                    </div>
                </div>
                <!-- end col -->

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <a href="layouts/auth-logout.html" target="_blank">
                            <img src="images/demo/logout.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </a>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Logout</h4>
                    </div>
                </div>
                <!-- end col -->
            </div>
            <!--end row-->
        </div>
        <!--end container-->
    </section>
    <!-- END SERVICE -->

    <!-- START SERVICE -->
    <section class="section" id="layouts">
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-lg-7">
                    <div class="header-title text-center">
                        <h3>Multiple color schemes & layouts</h3>
                        <div class="title-border mt-3"></div>
                        <p class="text-muted mt-3">Multiple style demos are available allowing to build web applications
                            with any need</p>
                    </div>
                </div>
                <!--end col-->
            </div>
            <!--end row-->

            <div class="row justify-content-center px-5">
                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/default.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Default Color Panel</h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-2.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 2 </h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-3.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 3</h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-4.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 4</h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-5.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 5</h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-6.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 6</h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-7.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 7</h4>
                    </div>
                </div>

                <div class="col-lg-4 col-md-6">
                    <div class="demo-box">
                        <div>
                            <img src="images/demo/color-8.jpg" alt="demo-img"
                                class="img-fluid home-dashboard border-light">
                        </div>
                    </div>
                    <div class="text-center">
                        <h4 class="fs-17 mt-4">Color Panel - 8</h4>
                    </div>
                </div>

            </div>
            <!--end row-->
        </div>
        <!--end container-->
    </section>
    <!-- END SERVICE -->


    <!-- START SERVICE -->
    <section class="section" id="features">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-7">
                    <div class="header-title text-center">
                        <p class="text-uppercase text-muted mb-2">Features We're Provided</p>
                        <h3>We do all Creative Features</h3>
                        <div class="title-border mt-3"></div>
                        <p class="text-muted mt-3">We are used following in our Chat App panel.</p>
                    </div>
                </div>
                <!--end col-->
            </div>
            <!--end row-->

            <div class="row">
                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/img-04.png" height="65" alt="">
                        <h5 class="fs-18 mt-4">Built with Bootstrap</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3">Chaton has the pure Bootstrap 5.3.0 framework crafted, clean, smart &
                            creative design.</p>
                    </div>
                </div>
                <!--end col-->


                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/dark-mode.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">Dark Mode</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">Chaton built-in light and dark layouts, select as per your
                            preference.</p>
                    </div>
                </div>
                <!--end col-->

                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/customize.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">Easy to customize</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">All the components are reusable and easy to customize it as
                            needs.</p>
                    </div>
                </div>
                <!--end col-->

                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/responsive-design.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">Fully Responsive</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">Chaton is fully responsive and comes with Bootstrap Framework</p>
                    </div>
                </div>
                <!--end col-->

                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/css.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">SASS Support</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">Built with Sass following a completely modular approach. Easy to
                            understand, light weight and extendible.</p>
                    </div>
                </div>
                <!--end col-->

                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/code.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">Clean Code</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">Clean & well commented codes structured and easy to understand
                        </p>
                    </div>
                </div>
                <!--end col-->


                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/task.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">Documentation</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">A nice documentation to help you get started fast</p>
                    </div>
                </div>
                <!--end col-->



                <div class="col-lg-3 col-md-6">
                    <div class="service-box text-center mt-4">
                        <img src="images/feature/update.png" alt="" class="img-fluid">
                        <h5 class="fs-18 mt-4">Lifetime Free Updates</h5>
                        <div class="lighlight-border mt-3"></div>
                        <p class="text-muted mt-3 mb-0">We provide Life time free Updates upto date package..</p>
                    </div>
                </div>
                <!--end col-->
            </div>
            <!--end row-->
        </div>
        <!--end container-->
    </section>
    <!-- END SERVICE -->


    <!-- START CTA -->
    <section class="bg-cta">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-10">
                    <div class="header-title text-center">
                        <h2>Chaton - Chat App Template</h2>
                        <p class="title-desc text-muted mt-3"> Start working with Chaton fast build dashboard
                            for any platform </p>
                        <div class="mt-4">
                            <a href="#demos" class="btn btn-primary">View Demos</a>
                        </div>
                    </div>

                </div>
                <!--end col-->
            </div>
            <!--end row-->
        </div>
        <!--end container-->
    </section>
    <!-- END CTA -->

    <!-- START CONTACT -->
    <section class="section" id="contact">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-7">
                    <div class="text-center mb-4">
                        <p class="text-uppercase text-muted mb-2">Contact</p>
                        <h3 class="text-uppercase">Get In Touch</h3>
                        <div class="title-border mt-3"></div>
                        <p class="title-desc text-muted mt-3">Our team is happy to help you. support DOES NOT include
                            template customization, installation or any third party software and plugins.</p>
                    </div>
                </div>
                <!--end col-->
            </div>
            <!--end row-->

            <div class="row justify-content-center">

                <div class="col-lg-9">
                    <div class="custom-form">
                        <form method="post" name="myForm" onsubmit="return validateForm()">
                            <p id="error-msg"></p>
                            <div class="row">
                                <div class="col-lg-12">
                                    <div class="mb-3">
                                        <label for="name" class="form-label">Name* :</label>
                                        <input name="name" id="name" type="text" class="form-control"
                                            placeholder="Enter your name">
                                    </div>
                                </div>
                                <!--end col-->
                            </div>
                            <!-- end row -->

                            <div class="row">
                                <div class="col-lg-6">
                                    <div class="mb-3">
                                        <label for="email" class="form-label">Email address* :</label>
                                        <input type="email" class="form-control" name="email" id="email"
                                            placeholder="Enter your email">
                                    </div>
                                </div>
                                <!-- end col -->

                                <div class="col-lg-6">
                                    <div class="mb-3">
                                        <label for="subject" class="form-label">Your Subject* :</label>
                                        <input type="tel" class="form-control" name="text" id="subject"
                                            placeholder="Enter your subject">
                                    </div>
                                </div>
                                <!-- end col -->

                                <div class="col-lg-12">
                                    <div class="mb-3">
                                        <label for="comments" class="form-label">Comments :</label>
                                        <textarea class="form-control" placeholder="Leave a comment here"
                                            name="comments" id="comments"></textarea>
                                    </div>
                                </div>
                                <!-- end col -->

                            </div>
                            <!-- end row -->

                            <div class="row">
                                <div class="col-lg-12">
                                    <div class="mt-3 text-end">
                                        <input type="submit" id="submit" name="send" class="submitBnt btn btn-primary"
                                            value="Send Message">
                                        <div id="simple-msg"></div>
                                    </div>
                                </div>
                                <!-- end col -->
                            </div>
                            <!-- end row -->
                        </form>
                        <!-- end form -->
                    </div>
                </div>
                <!-- end col -->
            </div>
            <!--end row-->
        </div>
        <!--end container-->
    </section>
    <!-- END CONTACT -->

    <!-- FOOTER-ALT -->
    <div class="footer py-3">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <div class="float-start pull-none">
                        <p class="text-white-50 mb-0">
                            <script>document.write(new Date().getFullYear())</script> © Chaton. Design by <a
                                href="https://1.envato.market/themesdesign" target="_blank" class="text-white-50">Themesdesign</a>
                        </p>
                    </div>

                </div>
                <!-- end col -->

                <div class="col-lg-6">
                    <div class="float-end pull-none">
                        <ul class="list-unstyled text-sm-end social-icon social mb-0">
                            <li class="list-inline-item mb-0"><a href="https://www.facebook.com/themesdesignstudio/"
                                    target="_blank" class="rounded"><i class="bi bi-facebook" title="Facebook"></i></a>
                            </li>
                            <li class="list-inline-item mb-0"><a href="https://dribbble.com/themesdesign"
                                    target="_blank" class="rounded"><i class="bi bi-dribbble" title="Instagram"></i></a>
                            </li>
                            <li class="list-inline-item mb-0"><a href="mailto:themesdesign.in@gmail.com" target="_blank"
                                    class="rounded"><i class="bi bi-envelope" title="Google +"></i></a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- end row -->
        </div>
        <!--end container-->
    </div>
    <!-- END FOOTER-ALT -->

    <!--start back-to-top-->
    <button onclick="topFunction()" id="back-to-top">
        <i class="bi bi-arrow-up fs-15"></i>
    </button>
    <!--end back-to-top-->

    <!-- Bootstrap Js -->
    <script src="js/bootstrap.bundle.min.js"></script>

    <!-- App Js -->
    <script src="js/app.js"></script>

</body>

</html>