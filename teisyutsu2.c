#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>

/* ================= 共通 ================= */

void write_tweet(FILE *fp, const char *text)
{
    if (text && strlen(text) > 0)
    {
        fprintf(fp, "%s\n---\n", text);
    }
}

void strip_newline(char *s)
{
    if (!s) return;
    s[strcspn(s, "\r\n")] = '\0';
}

/* ================= main ================= */

int main(void)
{
    setlocale(LC_ALL, "");

    /* 今日の日付 */
    time_t now = time(NULL);
    struct tm *lt = localtime(&now);
    char today[16];

    sprintf(today, "%d/%d/%d",
            lt->tm_year + 1900,
            lt->tm_mon + 1,
            lt->tm_mday);

    printf("today is %s\n", today);

    /* 出力ファイル（UTF-8 BOM付き） */
    FILE *out = fopen("info_tweet.txt", "wb");
    if (!out)
    {
        perror("info_tweet.txt");
        return 1;
    }

    unsigned char bom[] = {0xEF, 0xBB, 0xBF};
    fwrite(bom, 1, 3, out);

    fprintf(out, "🐸今日(%s)の蛙亭🐸\n", today);

    char buf[1024];
    char last[512] = "";
    int found = 0;
    int live_header = 0;

    /* ================= 劇場 ================= */

    FILE *fp = fopen("theater2026.csv", "rb");
    if (!fp)
    {
        perror("theater2026.csv");
        return 1;
    }

    fgets(buf, sizeof(buf), fp); /* ヘッダ */

    while (fgets(buf, sizeof(buf), fp))
    {
        char *token;
        int col = 0;
        char *title = NULL, *date = NULL, *place = NULL, *time = NULL;

        token = strtok(buf, ",");
        while (token)
        {
            strip_newline(token);
            col++;
            if (col == 1) title = token;
            if (col == 2) date  = token;
            if (col == 5) place = token;
            if (col == 6) time  = token;
            token = strtok(NULL, ",");
        }

        if (date && strcmp(date, today) == 0)
        {
            char outbuf[512] = "";

            if (!live_header)
            {
                strcat(outbuf, "【ライブ】\n");
                live_header = 1;
            }

            sprintf(outbuf + strlen(outbuf),
                    "%s\n@%s\n%s\n",
                    title, place, time);

            if (strcmp(outbuf, last) != 0)
            {
                write_tweet(out, outbuf);
                strcpy(last, outbuf);
                found = 1;
            }
        }
    }
    fclose(fp);

    /* ================= メディア ================= */

    fp = fopen("kaeruTV2026.csv", "rb");
    if (!fp)
    {
        perror("kaeruTV2026.csv");
        return 1;
    }

    fgets(buf, sizeof(buf), fp);
    strcpy(last, "");

    while (fgets(buf, sizeof(buf), fp))
    {
        char *token;
        int col = 0;
        char *title=NULL,*date=NULL,*from=NULL,*to=NULL,*station=NULL,*note=NULL;

        token = strtok(buf, ",");
        while (token)
        {
            strip_newline(token);
            col++;
            if (col == 1) title   = token;
            if (col == 2) date    = token;
            if (col == 3) from    = token;
            if (col == 4) to      = token;
            if (col == 5) station = token;
            if (col == 6) note    = token;
            token = strtok(NULL, ",");
        }

        if (date && strcmp(date, today) == 0)
        {
            char outbuf[512];
            sprintf(outbuf,
                    "【メディア】\n%s\n%s-%s\n@%s\n%s\n",
                    title, from, to, station, note);

            if (strcmp(outbuf, last) != 0)
            {
                write_tweet(out, outbuf);
                strcpy(last, outbuf);
                found = 1;
            }
        }
    }
    fclose(fp);

    /* ================= レギュラー ================= */

    if (lt->tm_wday == 3)
    {
        write_tweet(out,
            "【メディア】≪レギュラー≫\n"
            "これ余談なんですけど…\n"
            "@ABCテレビ\n23:10-24:17\n"
            "※イワクラさんのみ\n");
        found = 1;
    }

    if (lt->tm_wday == 0)
    {
        write_tweet(out,
            "【メディア】≪レギュラー≫\n"
            "ポケモンとどこ行く!?\n"
            "@テレビ東京\n7:30-8:30\n"
            "※中野さんのみ\n");
        found = 1;
    }

    /* ================= その他 ================= */

    fp = fopen("other.csv", "rb");
    if (!fp)
    {
        perror("other.csv");
        return 1;
    }

    fgets(buf, sizeof(buf), fp);
    strcpy(last, "");

    while (fgets(buf, sizeof(buf), fp))
    {
        char *token;
        int col = 0;
        char *title=NULL,*date=NULL,*content=NULL,*place=NULL,*note=NULL;

        token = strtok(buf, ",");
        while (token)
        {
            strip_newline(token);
            col++;
            if (col == 1) title   = token;
            if (col == 2) date    = token;
            if (col == 3) content = token;
            if (col == 5) place   = token;
            if (col == 6) note    = token;
            token = strtok(NULL, ",");
        }

        if (date && strcmp(date, today) == 0)
        {
            char outbuf[512];
            sprintf(outbuf,
                    "【その他】\n%s\n@%s\n%s\n%s\n",
                    title, place, content, note);

            if (strcmp(outbuf, last) != 0)
            {
                write_tweet(out, outbuf);
                strcpy(last, outbuf);
                found = 1;
            }
        }
    }
    fclose(fp);

    if (!found)
    {
        fprintf(out, "本日の予定はありません。\n");
    }

    fclose(out);
    return 0;
}
