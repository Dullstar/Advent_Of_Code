workspace "Advent_Of_Code"
    configurations {"debug", "release"}

project "Advent_Of_Code"
	kind "ConsoleApp"
	language "C++"
	architecture ("x86_64")
	cppdialect ("C++17")

	--dependencies
	files {"deps/fmt/include/**.h", "deps/fmt/src/format.cc", "deps/fmt/src/os.cc"}  -- fmt.cc is intentionally excluded
    files {"deps/dstr/include/**.h", "deps/dstr/src/**.cpp"}
	includedirs {"deps/fmt/include"}
    includedirs {"deps/dstr/include"}
	
	--project files
	files {"source/**.h", "source/**.cpp"}

    filter "configurations:debug"
        targetdir "bin-debug"
		defines {"DEBUG"}
		symbols "On"

    filter "configurations:release"
        targetdir "bin"
		optimize "Speed"

	filter "toolset:gcc or toolset:clang"  --todo: clang complains about -fmax-errors, but will compile anyway
		-- We want most warnings, but we specifically disable -Wunused-parameter because of how unimplemented days are handled.
		buildoptions {"-Wall", "-Wextra", "-pedantic", "-fmax-errors=5", "-Wno-unused-parameter"}
