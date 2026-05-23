<properties>
    <java.version>17</java.version>
    <testcontainers.version>1.19.3</testcontainers.version>
    <wiremock.version>3.3.1</wiremock.version>
</properties>

<dependencies>
    <!-- Spring Boot web (optional – only if you need it in your app) -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Testcontainers core -->
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers</artifactId>
        <version>${testcontainers.version}</version>
        <scope>test</scope>
    </dependency>

    <!-- WireMock image for Testcontainers -->
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>wiremock</artifactId>
        <version>${testcontainers.version}</version>
        <scope>test</scope>
    </dependency>

    <!-- WireMock Java API (used to build stubs) -->
    <dependency>
        <groupId>com.github.tomakehurst</groupId>
        <artifactId>wiremock-jre8</artifactId>
        <version>${wiremock.version}</version>
        <scope>test</scope>
    </dependency>

    <!-- JUnit 5 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>