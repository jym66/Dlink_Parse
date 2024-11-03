// const sm3 = require('sm3');
/*
 * JavaScript SM3
 * https://github.com/jiaxingzheng/JavaScript-SM3
 *
 * Copyright 2017, Zheng Jiaxing
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 *
 * Refer to
 * http://www.oscca.gov.cn/UpFile/20101222141857786.pdf
 */


// 左补0到指定长度
function leftPad(str, totalLength) {
    const len = str.length;
    return Array(totalLength > len ? ((totalLength - len) + 1) : 0).join(0) + str;
}

// 二进制转化为十六进制
function binary2hex(binary) {
    const binaryLength = 8;
    let hex = '';
    for (let i = 0; i < binary.length / binaryLength; i += 1) {
        hex += leftPad(parseInt(binary.substr(i * binaryLength, binaryLength), 2).toString(16), 2);
    }
    return hex;
}

// 十六进制转化为二进制
function hex2binary(hex) {
    const hexLength = 2;
    let binary = '';
    for (let i = 0; i < hex.length / hexLength; i += 1) {
        binary += leftPad(parseInt(hex.substr(i * hexLength, hexLength), 16).toString(2), 8);
    }
    return binary;
}

// utf16码点值转化为utf8二进制
function utf16CodePoint2utf8Binary(ch) {
    const utf8Arr = [];
    const codePoint = ch.codePointAt(0);

    if (codePoint >= 0x00 && codePoint <= 0x7f) {
        utf8Arr.push(codePoint);
    } else if (codePoint >= 0x80 && codePoint <= 0x7ff) {
        utf8Arr.push((192 | (31 & (codePoint >> 6))));
        utf8Arr.push((128 | (63 & codePoint)))
    } else if ((codePoint >= 0x800 && codePoint <= 0xd7ff)
        || (codePoint >= 0xe000 && codePoint <= 0xffff)) {
        utf8Arr.push((224 | (15 & (codePoint >> 12))));
        utf8Arr.push((128 | (63 & (codePoint >> 6))));
        utf8Arr.push((128 | (63 & codePoint)))
    } else if (codePoint >= 0x10000 && codePoint <= 0x10ffff) {
        utf8Arr.push((240 | (7 & (codePoint >> 18))));
        utf8Arr.push((128 | (63 & (codePoint >> 12))));
        utf8Arr.push((128 | (63 & (codePoint >> 6))));
        utf8Arr.push((128 | (63 & codePoint)))
    }

    let binary = '';
    for (let utf8Code of utf8Arr) {
        const b = utf8Code.toString(2);
        binary += leftPad(b, Math.ceil(b.length / 8) * 8);
    }

    return binary;
}

// 普通字符串转化为二进制
function str2binary(str) {
    let binary = '';
    for (const ch of str) {
        binary += utf16CodePoint2utf8Binary(ch);
    }
    return binary;
}

// 循环左移
function rol(str, n) {
    return str.substring(n % str.length) + str.substr(0, n % str.length);
}

// 二进制运算
function binaryCal(x, y, method) {
    const a = x || '';
    const b = y || '';
    const result = [];
    let prevResult;
    // for (let i = 0; i < a.length; i += 1) { // 小端
    for (let i = a.length - 1; i >= 0; i -= 1) { // 大端
        prevResult = method(a[i], b[i], prevResult);
        result[i] = prevResult[0];
    }
    // console.log(`x     :${x}\ny     :${y}\nresult:${result.join('')}\n`);
    return result.join('');
}

// 二进制异或运算
function xor(x, y) {
    return binaryCal(x, y, (a, b) => [(a === b ? '0' : '1')]);
}

// 二进制与运算
function and(x, y) {
    return binaryCal(x, y, (a, b) => [(a === '1' && b === '1' ? '1' : '0')]);
}

// 二进制或运算
function or(x, y) {
    return binaryCal(x, y, (a, b) => [(a === '1' || b === '1' ? '1' : '0')]);// a === '0' && b === '0' ? '0' : '1'
}

// 二进制与运算
function add(x, y) {
    const result = binaryCal(x, y, (a, b, prevResult) => {
        const carry = prevResult ? prevResult[1] : '0' || '0';
        if (a !== b) return [carry === '0' ? '1' : '0', carry];// a,b不等时,carry不变，结果与carry相反
        // a,b相等时，结果等于原carry，新carry等于a
        return [carry, a];
    });
    // console.log('x: ' + x + '\ny: ' + y + '\n=  ' + result + '\n');
    return result;
}

// 二进制非运算
function not(x) {
    return binaryCal(x, undefined, a => [a === '1' ? '0' : '1']);
}

function calMulti(method) {
    return (...arr) => arr.reduce((prev, curr) => method(prev, curr));
}

// function xorMulti(...arr) {
//   return arr.reduce((prev, curr) => xor(prev, curr));
// }

// 压缩函数中的置换函数 P1(X) = X xor (X <<< 9) xor (X <<< 17)
function P0(X) {
    return calMulti(xor)(X, rol(X, 9), rol(X, 17));
}

// 消息扩展中的置换函数 P1(X) = X xor (X <<< 15) xor (X <<< 23)
function P1(X) {
    return calMulti(xor)(X, rol(X, 15), rol(X, 23));
}

// 布尔函数，随j的变化取不同的表达式
function FF(X, Y, Z, j) {
    return j >= 0 && j <= 15 ? calMulti(xor)(X, Y, Z) : calMulti(or)(and(X, Y), and(X, Z), and(Y, Z));
}

// 布尔函数，随j的变化取不同的表达式
function GG(X, Y, Z, j) {
    return j >= 0 && j <= 15 ? calMulti(xor)(X, Y, Z) : or(and(X, Y), and(not(X), Z));
}

// 常量，随j的变化取不同的值
function T(j) {
    return j >= 0 && j <= 15 ? hex2binary('79cc4519') : hex2binary('7a879d8a');
}

// 压缩函数
function CF(V, Bi) {
    // 消息扩展
    const wordLength = 32;
    const W = [];
    const M = [];// W'

    // 将消息分组B划分为16个字W0， W1，…… ，W15 （字为长度为32的比特串）
    for (let i = 0; i < 16; i += 1) {
        W.push(Bi.substr(i * wordLength, wordLength));
    }

    // W[j] <- P1(W[j−16] xor W[j−9] xor (W[j−3] <<< 15)) xor (W[j−13] <<< 7) xor W[j−6]
    for (let j = 16; j < 68; j += 1) {
        W.push(calMulti(xor)(
            P1(calMulti(xor)(W[j - 16], W[j - 9], rol(W[j - 3], 15))),
            rol(W[j - 13], 7),
            W[j - 6]
        ));
    }

    // W′[j] = W[j] xor W[j+4]
    for (let j = 0; j < 64; j += 1) {
        M.push(xor(W[j], W[j + 4]));
    }

    // 压缩
    const wordRegister = [];// 字寄存器
    for (let j = 0; j < 8; j += 1) {
        wordRegister.push(V.substr(j * wordLength, wordLength));
    }

    let A = wordRegister[0];
    let B = wordRegister[1];
    let C = wordRegister[2];
    let D = wordRegister[3];
    let E = wordRegister[4];
    let F = wordRegister[5];
    let G = wordRegister[6];
    let H = wordRegister[7];

    // 中间变量
    let SS1;
    let SS2;
    let TT1;
    let TT2;
    for (let j = 0; j < 64; j += 1) {
        SS1 = rol(calMulti(add)(rol(A, 12), E, rol(T(j), j)), 7);
        SS2 = xor(SS1, rol(A, 12));

        TT1 = calMulti(add)(FF(A, B, C, j), D, SS2, M[j]);
        TT2 = calMulti(add)(GG(E, F, G, j), H, SS1, W[j]);

        D = C;
        C = rol(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = rol(F, 19);
        F = E;
        E = P0(TT2);
    }

    return xor(Array(A, B, C, D, E, F, G, H).join(''), V);
}

// sm3 hash算法 http://www.oscca.gov.cn/News/201012/News_1199.htm
function sm3(content) {
    let binary = ""
    if (typeof content == 'string') {
        binary = str2binary(content);
    } else {
        for (a of content) {
            binary += a.toString(2).padStart(8, "0")
        }
    }
    // 填充
    const len = binary.length;
    // k是满足len + 1 + k = 448mod512的最小的非负整数
    let k = len % 512;
    // 如果 448 <= (512 % len) < 512，需要多补充 (len % 448) 比特'0'以满足总比特长度为512的倍数
    k = k >= 448 ? 512 - (k % 448) - 1 : 448 - k - 1;
    const m = `${binary}1${leftPad('', k)}${leftPad(len.toString(2), 64)}`.toString();// k个0

    // 迭代压缩
    const n = (len + k + 65) / 512;

    let V = hex2binary('7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e');
    for (let i = 0; i <= n - 1; i += 1) {
        const B = m.substr(512 * i, 512);
        V = CF(V, B);
    }
    return binary2hex(V);
}


function hexToByteArray(hexString) {
    const byteArray = [];
    for (let i = 0; i < hexString.length; i += 2) {
        byteArray.push(parseInt(hexString.slice(i, i + 2), 16));
    }
    return byteArray;
}

function rc4_like(plaintext, key = "Ó") {
    const S = new Array(256); // S盒（置换数组）
    for (let i = 0; i < 256; i++) {
        S[i] = 255 - i;
    }
    let j = 0;
    for (let i = 0; i < 256; i++) {
        const temp = S[i];
        const product = j * S[i];
        let sum = product + j;
        const keyIndex = i % key.length;
        const keyCharCode = key.charCodeAt(keyIndex);
        sum += keyCharCode;
        j = sum % 256;
        S[i] = S[j];
        S[j] = temp;
    }
    let encryptedText = "";
    let encryptedArray = []
    let i = 0;
    j = 0;
    for (let index = 0; index < plaintext.length; index++) {
        i = (i + 1) % 256;
        const temp = S[i];
        j = (j + temp) % 256;
        // 交换 S[i] 和 S[j]
        S[i] = S[j];
        S[j] = temp;
        // 生成密钥流字节并加密
        const K = S[(S[i] + S[j]) % 256];
        // const charCode = plaintext.charCodeAt(index);
        const charCode = plaintext[index];
        const encryptedCharCode = charCode ^ K;
        // encryptedText += String.fromCharCode(encryptedCharCode);
        encryptedArray.push(encryptedCharCode)
    }
    return encryptedArray;

}


function encodeBase(input, base = "Dkdpgh2ZmsQB80/MfvV36XI1R45-WUAlEixNLwoqYTOPuzKFjJnry79HbGcaStCe") {
    function encodeString(str) {
        let binaryString = "";

        for (let i = 0; i < str.length; i++) {
            const binary = str.charCodeAt(i).toString(2).padStart(8, '0');
            binaryString += binary;
        }

        let encodedString = "";
        for (let i = 0; i < binaryString.length; i += 6) {
            const segment = binaryString.slice(i, i + 6).padEnd(6, '0');
            const index = parseInt(segment, 2);
            encodedString += base[index] || "=";
        }
        while (encodedString.length % 4 !== 0) {
            encodedString += "=";
        }

        return encodedString;
    }

    if (Array.isArray(input)) {
        const str = input.map(num => String.fromCharCode(num)).join('');
        return encodeString(str);
    } else if (typeof input === 'string') {
        return encodeString(input);
    } else {
        throw new TypeError("Input must be a string or an array of numbers.");
    }
}


function genHeard() {
    // 生成bog_us的头部
    let xor_array = [170, 85]
    let array = [3, 82]
    let result = []
    let random_num1 = (Math.random() * 1000) * 65535 & 255;
    let random_num2 = (Math.random() * 1000) * 40 >> 0;
    result.push(random_num1 & xor_array[0] | array[0] & xor_array[1])
    result.push(random_num1 & xor_array[1] | array[0] & xor_array[0])
    result.push(random_num2 & xor_array[0] | array[1] & xor_array[1])
    result.push(random_num2 & xor_array[1] | array[1] & xor_array[0])
    // return [139, 82, 112, 7]
    return result
}


function expandArrayTo132(arr, concat_array) {
    const xor_arr = [145, 110, 66, 189, 44, 211];
    let result = [];

    let random_num1;
    for (let i = 0; i < arr.length; i += 3) {
        random_num1 = (Math.random() * 1000) & 255;
        result.push((random_num1 & xor_arr[0]) | arr[i] & xor_arr[1])
        result.push((random_num1 & xor_arr[2]) | arr[i + 1] & xor_arr[3])
        result.push((random_num1 & xor_arr[4]) | arr[i + 2] & xor_arr[5])
        result.push((arr[i] & xor_arr[0]) | (arr[i + 1] & xor_arr[2]) | (arr[i + 2] & xor_arr[4]))
    }
    result = concat_array.concat(result)
    return result
}

function encty_time(time) {
    const str = ((time + 3) & 255) + ',';
    const timeArr = [];
    for (let i = 0; i < str.length; i++) {
        timeArr.push(str.charCodeAt(i))
    }
    return timeArr
}

function genArray(params_sm3, dhzx_sm3, ua_sm3, concat_array) {
    let envStr = "712|1271|2560|1392|2560|1392|2560|1440|Win32"
    let envArray = []
    let timestamp = new Date().getTime();
    let enc_time = encty_time(timestamp)
    let result = [1, 0, 70, 226, 0, 171, 0, 0, 1, 6, 1, 3, 51, 24, 23, 252, 146, 0, 226, 239, 7, 44, 0, 0, 7, 29, 0, 225, 6, 24, 1, 0, 25, 82, 3, 0, 146, 97, 177, 1, 1, 0, 0, 41, 156, 225, 45, 0, 4, 0]
    result[0] = (timestamp / 256 / 256 / 256 / 256 / 256) & 255
    result[1] = 0
    result[2] = ua_sm3[11]
    result[3] = timestamp >> 8 & 255
    result[4] = (6383 >> 16) & 255
    result[5] = timestamp & 255
    result[6] = (6241 >> 24) & 255
    result[7] = (0 >> 8) & 255
    result[8] = (1 % 256) & 255
    result[9] = params_sm3[18]
    result[10] = 1
    result[11] = 3
    result[12] = params_sm3[3]
    result[13] = (6241 >> 8) & 255
    result[14] = (20 + 3) & 255
    result[15] = params_sm3[9]
    result[16] = (timestamp / 256 * 4) & 255
    result[17] = 0 >> 24 & 255
    result[18] = timestamp >> 8 & 255
    result[19] = 6383 & 255
    result[20] = ((new Date().getTime() - 1721836800000) / 1000 / 60 / 60 / 24 / 14) >> 0
    result[21] = dhzx_sm3[4]
    result[22] = timestamp >> 16 & 255
    result[23] = (6241 >> 16) & 255
    result[24] = ua_sm3[5]
    result[26] = timestamp >> 16 & 255
    result[27] = timestamp >> 24 & 255
    result[28] = 6
    result[29] = 6383 >> 8 & 255
    result[31] = 6383 >> 24 & 255
    result[32] = ua_sm3[21]
    result[33] = dhzx_sm3[10]
    result[36] = (timestamp / 256 * 4) & 255
    result[37] = 6241 & 255
    result[38] = dhzx_sm3[19]
    result[40] = (timestamp / 256 * 5) & 255
    result[41] = 0
    result[42] = 1 / 256 & 255
    result[43] = 41
    result[44] = timestamp & 255
    result[45] = timestamp >> 24 & 255
    result[46] = envStr.length & 255
    result[47] = envStr.length >> 8 & 255
    result[48] = enc_time.length & 255
    result[49] = enc_time.length >> 8 & 255

    let check_num = 0
    check_array = concat_array.concat(result)
    for (let i = 0; i < check_array.length; i++) {
        check_num ^= check_array[i]
    }

    for (let i = 0; i < envStr.length; i++) {
        envArray.push(envStr.charCodeAt(i))
    }
    // 时间戳数组拼接到环境后边
    envArray = envArray.concat(enc_time).concat([check_num])
    result = result.concat(envArray);
    return result
}


function get_a_bogus(params, ua) {
    const params_sm3 = hexToByteArray(sm3(hexToByteArray(sm3(params + "dhzx"))));
    const dhzx_sm3 = hexToByteArray(sm3(hexToByteArray(sm3("dhzx"))));
    ua_array = []
    for (let i = 0; i < ua.length; i++) {
        ua_array.push(ua.charCodeAt(i))
    }
    const ua_sm3 = hexToByteArray(sm3(encodeBase(rc4_like(ua_array, key = '\x00\x01\x00'), base = "ckdp1h4ZKsUB80/Mfvw36XIgR25+WQAlEi7NLboqYTOPuzmFjJnryx9HVGDaStCe")))
    concat_array = [35, 16, 0, 5, 1, 0, 170, 85]
    raw_array = genArray(params_sm3, dhzx_sm3, ua_sm3, concat_array)
    result = expandArrayTo132(raw_array, concat_array)
    rc4 = genHeard().concat(rc4_like(result))
    console.log(encodeBase(rc4))
    return encodeBase(rc4)
}

