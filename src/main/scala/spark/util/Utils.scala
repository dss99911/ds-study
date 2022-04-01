package spark.util

import org.apache.spark.sql.types.{StructField, StructType}
import org.apache.spark.sql.{Column, DataFrame}

object Utils {
  implicit class DataFrameExtensions(df: DataFrame) {
    def toUnderscoresFromCamelCase(): DataFrame = {
      def camelToUnderscores(name: String) = "[A-Z\\d]".r.replaceAllIn(name, { m =>
        "_" + m.group(0).toLowerCase()
      })

      df.columns.foldLeft(df)((df: DataFrame, colName: String) => df.withColumnRenamed(colName, camelToUnderscores(colName)))
    }

    def toCamelCaseFromUnderscores(): DataFrame = {
      def underscoreToCamel(s: String): String = {
        val split = s.split("_")
        val tail = split.tail.map { x => x.head.toUpper + x.tail }
        split.head + tail.mkString
      }

      df.columns.foldLeft(df)((df: DataFrame, colName: String) => df.withColumnRenamed(colName, underscoreToCamel(colName)))
    }


    def flattenColumns(): DataFrame = {
      def recurColumns(prefix: String, prefixRename: String, schema: StructField): Seq[Column] = {
        schema match {
          case StructField(name, dtype: StructType, _, _) =>
            dtype.fields.flatMap(recurColumns(name + ".", name + "_", _))

          case StructField(name, _, _, _) =>
            Seq(df.col(prefix + name).as(prefixRename + name))
        }
      }
      df.select(df.schema.fields.flatMap(recurColumns("", "", _)):_*)

    }

  }

  implicit class ColExtensions(c: Column) {
    def isNullOrEmpty: Column = {
      c.isNull or (c === lit(""))
    }
  }
}
