ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.15"

lazy val sparkVersion = "3.5.7"

lazy val root = (project in file("."))
  .settings(
    name := "procesamiento_datos",
    idePackagePrefix := Some("com.juan.procesamientodatos"),
      libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % sparkVersion,
      "org.apache.spark" %% "spark-sql"  % sparkVersion
    )
  )
