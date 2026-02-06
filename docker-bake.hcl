variable "registry" {
  default = "ghcr.io/r-bar"
}

group "default" {
  targets = [
    "esh",
    "haskell-language-server",
    "jsonnet-language-server",
    "mumble",
    "sumy_0-10",
    "utility",
    "vscode-langservers",
  ]
}


target "esh" {
  tags = [
    "${registry}/esh:0.3.2",
    "${registry}/esh:latest",
  ]
  dockerfile = "Dockerfile"
  context = "images/esh"
  args = {
    VERSION = "0.3.2",
  }
}

target "haskell-language-server" {
  tags = [
    "${registry}/haskell-language-server:1.7.0.0",
    "${registry}/haskell-language-server:latest",
  ]
  dockerfile = "Dockerfile"
  context = "images/haskell-language-server"
  args = {
    UBUNTU_VERSION = "22.04"
    GHC_VERSION = "9.2.1"
    HLS_VERSION = "1.7.0.0"
  }
}

target "jsonnet-language-server" {
  tags = [
    "${registry}/jsonnet-language-server:0.7.2",
    "${registry}/jsonnet-language-server:latest",
  ]
  dockerfile = "Dockerfile"
  context = "images/jsonnet-language-server"
  args = {
    VERSION = "0.7.2"
    OS = "linux"
    ALPINE_VERSION = "3.16"
    ARCH = "amd64"
  }
}

target "mumble" {
  tags = [
    "${registry}/mumble:1.3.0",
    "${registry}/mumble:latest",
  ]
  dockerfile = "Dockerfile"
  context = "images/mumble"
}


group "sumy" {
  targets = ["sumy:0.8", "sumy:0.10"]
}

target "sumy_0-8" {
  tags = [
    "${registry}/sumy:0.8.1",
  ]
  dockerfile = "Dockerfile"
  context = "images/sumy"
}

target "sumy_0-10" {
  tags = [
    "${registry}/sumy:0.10.0",
    "${registry}/sumy:latest",
  ]
  dockerfile = "Dockerfile"
  context = "images/sumy"
}

target "utility" {
  tags = [
    "${registry}/utility:latest",
  ]
  dockerfile = "Dockerfile"
  context = "images/utility"
}

target "vscode-langservers" {
  tags = [
    "${registry}/vscode-langservers:latest",
    "${registry}/vscode-langservers:4.2.1",
  ]
  dockerfile = "Dockerfile"
  context = "images/vscode-langservers"
  args = {
    "NODE_VERSION" = "18"
    "LANGSERVERS_VERSION" = "4.2.1"
  }
}
