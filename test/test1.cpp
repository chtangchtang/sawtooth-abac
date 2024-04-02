#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/wait.h>
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
    string filename = "yourfile.txt";

    int numProcesses = 1000;

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

    return 0;
}
