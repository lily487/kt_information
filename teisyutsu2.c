#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>

// ツイートを区切って書き込む
void write_tweet(FILE *fp, const char *text)
{
    if (text && strlen(text) > 0)
    {
        fprintf(fp, "%s\n---\n", text);
    }
}

int main(void)
{
    setlocale(LC_ALL, "");

    /* 今日の日付取得 */
    time_t currentTime = time(NULL);
    struct tm *localTime = localtime(&currentTime);
    char today[20];

    sprintf(today, "%d/%d/%d",
            localTime->tm_year + 1900,
            localTime->tm_mon + 1,
            localTime->tm_mday);

    printf("today is %s\n", today);

    FILE *fp1, *fp2, *fp3, *fp4;
    char buffer[1024];
    int found_any = 0;
    int live = 0;

    /* 出力ファイル */
    fp4 = fopen("info_tweet.txt", "w");
    if (!fp4)
    {
        printf("can't open info_tweet.txt\n");
        exit(1);
    }

    fprintf(fp4, "🐸今日(%s)の蛙亭🐸\n", today);

    /* ================= 劇場情報 ================= */
    fp1 = fopen("theater2026.csv", "r");
    if (!fp1)
    {
        printf("can't open theater2026.csv\n");
        exit(1);
    }

    fgets(buffer, sizeof(buffer), fp1); // ヘッダ読み飛ばし

    char last_output[512] = "";

    while (fgets(buffer, sizeof(buffer), fp1))
    {
        char *token;
        int col = 0;
        char *title = NULL, *date = NULL, *place = NULL, *time = NULL;

        token = strtok(buffer, ",");
        while (token)
        {
            token[strcspn(token, "\r\n")] = '\0';
            col++;

            if (col == 1) title = token;
            if (col == 2) date  = token;
            if (col == 5) place = token;
            if (col == 6) time  = token;

            token = strtok(NULL, ",");
        }

        if (date && strcmp(date, today) == 0)
        {
            char out[512] = "";

            if (!live)
            {
                strcat(out, "【ライブ】\n");
                live = 1;
            }

            sprintf(out + strlen(out), "%s\n@%s\n%s\n",
                    title, place, time);

            if (strcmp(out, last_output) != 0)
            {
                write_tweet(fp4, out);
                strcpy(last_output, out);
                found_any = 1;
            }
        }
    }
    fclose(fp1);

    /* ================= メディア情報 ================= */
    fp2 = fopen("kaeruTV2026.csv", "r");
    if (!fp2)
    {
        printf("can't open kaeruTV2026.csv\n");
        exit(1);
    }

    fgets(buffer, sizeof(buffer), fp2);
    strcpy(last_output, "");

    while (fgets(buffer, sizeof(buffer), fp2))
    {
        char *token;
        int col = 0;
        char *title = NULL, *date = NULL, *from = NULL, *to = NULL, *station = NULL, *note = NULL;

        token = strtok(buffer, ",");
        while (token)
        {
            token[strcspn(token, "\r\n")] = '\0';
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
            char out[512];
            sprintf(out, "【メディア】\n%s\n%s-%s\n@%s\n%s\n",
                    title, from, to, station, note);

            if (strcmp(out, last_output) != 0)
            {
                write_tweet(fp4, out);
                strcpy(last_output, out);
                found_any = 1;
            }
        }
    }
    fclose(fp2);

    /* ================= レギュラー ================= */
    if (localTime->tm_wday == 3)
    {
        write_tweet(fp4,
            "【メディア】≪レギュラー≫\n"
            "これ余談なんですけど…\n"
            "@ABCテレビ\n23:10-24:17\n"
            "※イワクラさんのみ\n");
        found_any = 1;
    }

    if (localTime->tm_wday == 0)
    {
        write_tweet(fp4,
            "【メディア】≪レギュラー≫\n"
            "ポケモンとどこ行く!?\n"
            "@テレビ東京\n7:30-8:30\n"
            "※中野さんのみ\n");
        found_any = 1;
    }

    /* ================= その他 ================= */
    fp3 = fopen("other.csv", "r");
    if (!fp3)
    {
        printf("can't open other.csv\n");
        exit(1);
    }

    fgets(buffer, sizeof(buffer), fp3);
    strcpy(last_output, "");

    while (fgets(buffer, sizeof(buffer), fp3))
    {
        char *token;
        int col = 0;
        char *title = NULL, *date = NULL, *content = NULL, *place = NULL, *note = NULL;

        token = strtok(buffer, ",");
        while (token)
        {
            token[strcspn(token, "\r\n")] = '\0';
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
            char out[512];
            sprintf(out, "【その他】\n%s\n@%s\n%s\n%s\n",
                    title, place, content, note);

            if (strcmp(out, last_output) != 0)
            {
                write_tweet(fp4, out);
                strcpy(last_output, out);
                found_any = 1;
            }
        }
    }
    fclose(fp3);

    if (!found_any)
    {
        fprintf(fp4, "本日の予定はありません。\n");
    }

    fclose(fp4);
    return 0;
}
