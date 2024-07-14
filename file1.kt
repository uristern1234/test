import java.time.LocalDateTime
import java.time.ZoneId
import java.time.ZonedDateTime

fun printDateTimeWithSystemDefaultZone(dateTime: LocalDateTime) {
    val systemDefaultZone = ZoneId.systemDefault()
    val zonedDateTime = ZonedDateTime.of(dateTime, systemDefaultZone)
    println("ZonedDateTime with system default zone: $zonedDateTime")
}

fun main() {
    val dateTime = LocalDateTime.now()
    printDateTimeWithSystemDefaultZone(dateTime)
}
