#include <iostream>
#include <sstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
// #include <influxdblpt.h>
// #include <influxdb.h>
#include <chrono>
#include <ctime>
#include <vector>

int main() {
    // 创建InfluxDB客户端
    // influxdb::InfluxDB db("http://172.21.105.145:8086", "metrics", "admin", "admin");
    // 获取当前的epoch时间
    // auto epoch_time = std::chrono::system_clock::now().time_since_epoch();
    // long long epoch_seconds = std::chrono::duration_cast<std::chrono::seconds>(epoch_time).count();
    // 创建数据点
    // std::string measurement = "start_test_add_policy";
    // std::map<std::string, std::string> fields = {{"epoch_time", std::to_string(epoch_seconds)}};
    // influxdb::Point point(measurement, fields);
    // 写入数据点到数据库
    // db.writePoint(point);

    auto epoch_time = std::chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds = std::chrono::duration_cast<std::chrono::seconds>(epoch_time).count();
    std::cout << "epoch_seconds: " << std::to_string(epoch_seconds) << std::endl;
    
    int maxConcurrentProcesses;
    std::cout << "请输入并发进程数：";
    std::cin >> maxConcurrentProcesses;

    std::string ip;
    std::cout << "请输入IP地址：";
    std::cin >> ip;

    std::vector<pid_t> childProcesses;

    for (int i = 1; i <= 100; ++i) {
        std::ostringstream oss;
        oss << i;
        std::string command = "abac add data/policy" + oss.str() + ".json --url " + ip;

        if (childProcesses.size() >= maxConcurrentProcesses) {
            // 等待子进程中的一个完成
            int status;
            waitpid(childProcesses.front(), &status, 0);
            // 删除已完成的子进程
            childProcesses.erase(childProcesses.begin());
        }

        pid_t childPid = fork();
        if (childPid == 0) {
            // 子进程执行命令
            execlp("sh", "sh", "-c", command.c_str(), NULL);
            return 0;
        } else {
            childProcesses.push_back(childPid);
        }
    }

    // 等待所有子进程结束
    for (pid_t childPid : childProcesses) {
        int status;
        waitpid(childPid, &status, 0);
    }

    std::cout << "epoch_seconds: " << std::to_string(epoch_seconds) << std::endl;
    
    auto epoch_time = std::chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds = std::chrono::duration_cast<std::chrono::seconds>(epoch_time).count();
    std::cout << "epoch_seconds: " << std::to_string(epoch_seconds) << std::endl;
    
    return 0;
}
