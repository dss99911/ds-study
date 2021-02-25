package spark;

import java.io.Serializable;

public class JavaClass implements Serializable {
    int ten;
    int value;

    public int getTen() {
        return ten;
    }

    public JavaClass setTen(int ten) {
        this.ten = ten;
        return this;
    }

    public int getValue() {
        return value;
    }

    public JavaClass setValue(int value) {
        this.value = value;
        return this;
    }
}