#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/wait.h>
#include <chrono>
using namespace std;

void readFromFile(const string& filename) {
    ifstream file(filename);
    if (file) {
        // 读取文件中的数据
        string content((istreambuf_iterator<char>(file)), (istreambuf_iterator<char>()));

        // 在控制台打印读取的数据
        // cout << "Child process " << getpid() << " read: " << content << endl;

        // 关闭文件
        file.close();
    } else {
        cerr << "Error opening file " << filename << endl;
    }
}

int main() {
    string filename = "data/inquiry.json";

    int numProcesses = 1000;
    auto epoch_time = chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds = chrono::duration_cast<chrono::seconds>(epoch_time).count();
    // 创建一千个子进程来读取文件的全部内容
    for (int i = 0; i < numProcesses; ++i) {
        pid_t pid = fork();
        if (pid == 0) {
            // 子进程读取文件的全部内容
            readFromFile(filename);
            return 0;
        } else if (pid < 0) {
            cerr << "Error forking process" << endl;
            return 1;
        }
    }

    // 等待所有子进程结束
    for (int i = 0; i < numProcesses; ++i) {
        wait(NULL);
    }
    auto epoch_time1 = chrono::system_clock::now().time_since_epoch();
    long long epoch_seconds1 = chrono::duration_cast<chrono::seconds>(epoch_time1).count();
    cout << "Time elapsed: " << epoch_seconds1 - epoch_seconds << " seconds" << endl;
    return 0;
}
