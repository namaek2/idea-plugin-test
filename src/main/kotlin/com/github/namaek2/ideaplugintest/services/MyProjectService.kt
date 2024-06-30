package com.github.namaek2.ideaplugintest.services

import com.github.namaek2.ideaplugintest.MyBundle
import com.intellij.openapi.components.Service
import com.intellij.openapi.diagnostic.thisLogger
import com.intellij.openapi.project.Project

@Service(Service.Level.PROJECT)
class MyProjectService(project: Project) {
    private val projectFolder = project.basePath
    init {
        thisLogger().info(MyBundle.message("projectService", project.name))
        //thisLogger().warn("Don't forget to remove all non-needed sample code files with their corresponding registration entries in `plugin.xml`.")
    }

    fun runPythonTask() {
        val javaFilesPath = projectFolder
        val outFolder = projectFolder
        val pythonScript = PythonScript()
        if (javaFilesPath != null) {
            if (outFolder != null) {
                pythonScript.runPythonScript(javaFilesPath, outFolder)
            } else {
                thisLogger().error(MyBundle.message("noOutputFolder"))
            }
        }
    }

    fun getRandomNumber() = (1..100).random()
}
