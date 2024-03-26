#include <iostream>
#include <sstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
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

    return 0;
}
