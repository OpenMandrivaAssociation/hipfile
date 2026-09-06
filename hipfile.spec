# GPU-direct storage (cuFile-shaped HIP API). TheRock 10.0.

Name:		hipfile
Version:	10.0.0
Release:	1
Summary:	HIP GPU-direct storage library
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-systems
Source0:	%{rocm_systems_source hipfile}

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	cmake(rocprofiler-register)
BuildRequires:	pkgconfig(mount)

ExclusiveArch:	%{x86_64} %{aarch64}

%description
hipFile is the HIP counterpart of NVIDIA cuFile: GPU-direct I/O between
storage and device memory. PyTorch USE_CUFILE and rocprofiler hipFile
tracing depend on libhipfile.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel

%description devel
Headers and CMake package for hipFile.

%prep
%autosetup -n hipfile -p1

%build
export CXX=hipcc
export CC=clang
%cmake %{rocm_cmake_fhs} \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DBUILD_SHARED_LIBS=ON \
	-DAIS_INSTALL_EXAMPLES=OFF \
	-DAIS_INSTALL_TOOLS=ON \
	-DAIS_INSTALL_TESTS=OFF \
	-DHIPFILE_ROCPROFILER_REGISTER=ON \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/hipfile ] && [ ! -d %{buildroot}%{_libdir}/cmake/hipfile ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/hipfile %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md CHANGELOG.md
%{_libdir}/libhipfile.so.*
%{_bindir}/ais-stats
%exclude %{_docdir}/hipfile/LICENSE.md

%files devel
%{_includedir}/hipfile.h
%{_includedir}/hipfile-api-trace.h
%{_libdir}/libhipfile.so
%{_libdir}/cmake/hipfile/
