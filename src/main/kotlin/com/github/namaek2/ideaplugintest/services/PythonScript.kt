package com.github.namaek2.ideaplugintest.services
import java.io.File
import java.io.IOException

class PythonScript {

    fun runPythonScript(javaFilesPath: String, outputFolder: String) {
        val scriptPath = "idea-plugin-test/pyscr/test.py" // Python 스크립트의 경로를 지정하세요.

        // ProcessBuilder를 사용하여 프로세스를 설정합니다.
        val processBuilder = ProcessBuilder("python", scriptPath, javaFilesPath, outputFolder)

        // 현재 작업 디렉토리를 설정할 수 있습니다.
        processBuilder.directory(File(System.getProperty("user.home")))

        // 프로세스의 출력을 캡처할 수 있도록 리디렉션합니다.
        processBuilder.redirectErrorStream(true)

        try {
            // 프로세스를 시작합니다.
            val process = processBuilder.start()

            // 프로세스의 출력을 읽습니다.
            val reader = process.inputStream.bufferedReader()
            val output = StringBuilder()
            reader.useLines { lines -> lines.forEach { output.append(it).append("\n") } }

            // 프로세스가 종료될 때까지 대기합니다.
            val exitCode = process.waitFor()

            // 프로세스의 종료 코드를 출력합니다.
            println("Process exited with code: $exitCode")
            // 프로세스의 출력을 출력합니다.
            println("Process output:\n$output")

        } catch (e: IOException) {
            e.printStackTrace()
        } catch (e: InterruptedException) {
            e.printStackTrace()
        }
    }
}
